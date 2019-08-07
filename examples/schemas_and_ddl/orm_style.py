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


class Baker(Base):
    __tablename__ = "baker"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    pronouns = Column(String)
    contact_id = Column(Integer, ForeignKey("contact_info.id"))


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
    birthday = Column(Date)


def walkthrough():
    breakpoint()
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
