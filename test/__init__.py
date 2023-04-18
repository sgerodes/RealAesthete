from dotenv import load_dotenv
load_dotenv()
from configuration import configure_logging, dot_items_globally
import os


configure_logging()
dot_items_globally()
os.environ['DB_CONNECTION_STRING'] = 'sqlite:///:memory:'  # in memory
