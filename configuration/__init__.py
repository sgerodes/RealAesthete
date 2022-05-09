from dotenv import load_dotenv
from .logging_configuration import configure_logging


def configure_project():
    load_dotenv()
    configure_logging()


configure_project()
