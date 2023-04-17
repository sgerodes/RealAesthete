from dotenv import load_dotenv
load_dotenv()
from scrapy_dot_items import dot_items_globally
from .logging_configuration import configure_logging
from .sqlalchemy_configuration import configure_sqlalchemy
from.playwright_configuration import configure_playwright



def configure_project():
    configure_logging()
    dot_items_globally()
    configure_sqlalchemy()
    # configure_playwright()
