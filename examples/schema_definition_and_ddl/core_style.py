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
    Column(Integer, primary_key=True),
    Column(String, nullable=False),
    Column(String, nullable=False),
    Column(Date),
)

baker = Table(
    "baker",
    metadata,
    Column(Integer, primary_key=True),
    Column(String, nullable=False),
    Column(String),
    Column(Integer, ForeignKey("contact_info.id")),
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
    Column(Integer, primary_key=True),
    Column(String, nullable=False),
    Column(Boolean),
    Column(Numeric),
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
    Column(Integer, primary_key=True),
    Column(Integer),
    Column(String, nullable=False),
    insta_handle=Column(String),
)
