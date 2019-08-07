from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    Date,
    ForeignKey,
    Numeric,
    Boolean,
    MetaData,
)

metadata = MetaData()


baker = Table(
    "baker",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("pronouns", String),
)


bread = Table(
    "bread",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("is_delicious", Boolean),
    Column("ingredient_cost", Numeric),
)

baker_specialty = Table(
    "baker_specialty",
    metadata,
    Column("baker_id", ForeignKey("baker.id"), primary_key=True),
    Column("bread_id", ForeignKey("bread.id"), primary_key=True),
)


contact_info = Table(
    "contact_info",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("baker_id", Integer, ForeignKey("baker.id")),
    Column("phone", Integer),
    Column("email", String, nullable=False),
    Column("insta_handle", String),
    Column("birthday", Date),
)


def walkthrough(engine):
    breakpoint()
    metadata.create_all(engine)
