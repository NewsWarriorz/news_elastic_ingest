import sys

import click

from news_elastic_ingest import index_bulk


@click.command()
@click.argument(
    "json_file",
    type=click.File(mode="r", lazy=True),
)
@click.option(
    "-i",
    "--indexprefix",
    required=False,
    default="news",
    help="elasticsearch index prefix",
)
@click.option(
    "-h",
    "--host",
    required=True,
    help="elasticsearch host ip/dns",
)
@click.option(
    "-p",
    "--password",
    required=True,
    help="elasticsearch password",
)
def main(json_file, indexprefix, host, password):
    index_bulk(json_file.read(), indexprefix, host, password)


if __name__ == "__main__":
    sys.exit(main())
