from persistence.models import Base, engine

Base.metadata.create_all(engine)