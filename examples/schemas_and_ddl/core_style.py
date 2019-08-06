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

bakery = Table(
    "bakery",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("location", String, nullable=False),
    Column("founded_date", Date),
)

baker = Table(
    "baker",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("pronouns", String),
    Column("contact_id", Integer, ForeignKey("contact_info.id")),
)

bakery_employees = Table(
    "bakery_employees",
    metadata,
    Column("baker_id", ForeignKey("baker.id"), primary_key=True),
    Column("bakery_id", ForeignKey("bakery.id"), primary_key=True),
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
    Column("phone", Integer),
    Column("email", String, nullable=False),
    Column("insta_handle", String),
)
