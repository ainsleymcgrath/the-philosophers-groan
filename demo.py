from sqlalchemy import create_engine, MetaData
from examples import schemas_and_ddl, querying

engine = create_engine("sqlite://")
metadata = MetaData(bind=engine)

schemas_and_ddl.orm_style.create_all(engine)
querying.orm_style.walkthrough(engine)

metadata.drop_all()

schemas_and_ddl.core_style.create_all(engine)
querying.core_style.walkthrough(engine)

metadata.drop_all()
