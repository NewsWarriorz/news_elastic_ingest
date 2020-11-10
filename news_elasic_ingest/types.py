from elasticsearch_dsl import Document, Date, Text, analyzer, tokenizer

stop_stem_analyzer = analyzer(
    "stop_stem_analyzer",
    tokenizer=tokenizer("standard"),
    filter=["lowercase", "stop", "porter_stem"],
)


def get_article_class(index: str) -> Document:
    """
    Generate new Article class for specific index name and call init().

    Article
    -------
    title: Text(analyse)
        Article's title
    content: Text(analyse)
        Article's content
    published_date: Date
        Article's publish date
    url: Text
        Article's url

    Note
    ----
    Make sure that connection to elastic exist before calling this,
    to establish connection use `connect` function
    """

    class Article(Document):
        title = Text(analyzer=stop_stem_analyzer)
        content = Text(analyzer=stop_stem_analyzer)
        published_date = Date()
        url = Text()

        class Index:
            name = index

    Article.init()
    return Article
