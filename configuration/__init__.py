from dotenv import load_dotenv
from scrapy_dot_items import dot_items_globally
from .logging_configuration import configure_logging
from .sqlalchemy_configuration import configure_sqlalchemy
from . import fake_user_agents_fix


def configure_project():
    load_dotenv()
    configure_logging()
    dot_items_globally()
    configure_sqlalchemy()
