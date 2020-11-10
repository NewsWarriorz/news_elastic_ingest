import json
import logging
import urllib
from datetime import datetime

from elasticsearch.helpers import bulk as _bulk
from elasticsearch_dsl.connections import connections

from .types import get_article_class

__author__ = "Ashutosh Varma <ashutoshvarma11@live.com>"
__license__ = "MIT"
__version__ = (
    __import__("pkg_resources")
    .resource_string(__name__, "_version.txt")
    .decode("utf-8")
    .strip()
)

logger = logging.getLogger(__name__)


CLIENT = None


def connect(host, password):
    global CLIENT
    CLIENT = connections.create_connection(
        hosts=[
            host,
        ],
        http_auth=("elastic", password),
    )
    return CLIENT


def bulk(client, actions, stats_only=False, *args, **kwargs):
    include_meta = kwargs.pop("include_meta", True)
    skip_empty = kwargs.pop("skip_empty", True)
    actions = (
        i.to_dict(include_meta=include_meta, skip_empty=skip_empty) for i in actions
    )
    return _bulk(client, actions)


def index_bulk(json_data, index="newsbasic", host=None, password=None):
    """
    Create Articles from `json_data` and upload to elasticsearch at `host` with
    `index`.

    Parameters
    ----------
    josn_data: str
        string with valid JSON encoded articles in each line.
        (Dumped from crawlers)
    index: str
        elasticsearch index, will be created if not existed.
    host: str
        elasticsearch host, optional if connection already established
        using `connect` function
    password: str
        elasticsearch password, optional if connection already established
        using `connect` function
    """
    global CLIENT
    if not CLIENT:
        CLIENT = connections.create_connection(
            hosts=[
                host,
            ],
            http_auth=("elastic", password),
        )
    Article = get_article_class(index)
    articles = []
    for line in json_data:
        if line != "\n":
            article_json = json.loads(line)
            article = Article(
                meta={"id": urllib.parse.quote(article_json["link"]["url"])},
                title=article_json["link"]["title"],
                content=article_json["content"],
                published_date=datetime.strptime(
                    article_json["link"]["date"], "%Y-%m-%d"
                ),
                url=article_json["link"]["url"],
            )
            articles.append(article)
    logger.info(
        f"Uploading {len(articles)} articles to Elasticsearch server at {host}:9200"
    )
    bulk(CLIENT, articles, include_meta=True)
