import warnings
from sqlalchemy.exc import SAWarning


def configure_sqlalchemy():
    warnings.filterwarnings('ignore',
     r"^Dialect sqlite\+pysqlite does \*not\* support Decimal objects natively\, "
     "and SQLAlchemy must convert from floating point - rounding errors and other "
     "issues may occur\. Please consider storing Decimal numbers as strings or "
     "integers on this platform for lossless storage\.$",
     SAWarning, r'^sqlalchemy\.sql\.type_api$')
