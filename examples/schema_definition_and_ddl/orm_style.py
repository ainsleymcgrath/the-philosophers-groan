from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    Date,
    ForeignKey,
    Numeric,
    Boolean,
    create_engine,
)


Base = declarative_base()


class Bakery(Base):
    __tablename__ = "bakery"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    founded_date = Column(Date)


class Baker(Base):
    __tablename__ = "baker"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    pronouns = Column(String)
    contact_id = Column(Integer, ForeignKey("contact_info.id"))


bakery_employees = Table(
    "bakery_employees",
    Base.metadata,
    Column("baker_id", ForeignKey("baker.id"), primary_key=True),
    Column("bakery_id", ForeignKey("bakery.id"), primary_key=True),
)


class Bread(Base):
    __tablename__ = "bread"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_delicious = Column(Boolean)
    ingredient_cost = Column(Numeric)


baker_specialty = Table(
    "baker_specialty",
    Base.metadata,
    Column("baker_id", ForeignKey("baker.id"), primary_key=True),
    Column("bread_id", ForeignKey("bread.id"), primary_key=True),
)


class ContactInfo(Base):
    __tablename__ = "contact_info"

    id = Column(Integer, primary_key=True)
    phone = Column(Integer)
    email = Column(String, nullable=False)
    insta_handle = Column(String)
