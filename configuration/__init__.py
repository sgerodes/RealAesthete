from dotenv import load_dotenv
from .logging_configuration import configure_logging
from scrapy_dot_items import dot_items_globally


def configure_project():
    load_dotenv()
    configure_logging()
    dot_items_globally()


configure_project()
