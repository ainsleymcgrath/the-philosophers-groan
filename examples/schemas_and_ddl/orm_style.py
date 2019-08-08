from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    Date,
    ForeignKey,
    Numeric,
    Boolean,
)


Base = declarative_base()


class ContactInfo(Base):
    __tablename__ = "contact_info"

    id = Column(Integer, primary_key=True)
    phone = Column(Integer)
    email = Column(String, nullable=False)
    insta_handle = Column(String)
    birthday = Column(Date)
    baker_id = Column(Integer, ForeignKey("baker.id"))
    baker = relationship("Baker", back_populates="contact")

    def __repr__(self):
        return f"<ContactInfo {self.baker.name} {self.insta_handle}>"


baker_specialty = Table(
    "baker_specialty",
    Base.metadata,
    Column("baker_id", ForeignKey("baker.id"), primary_key=True),
    Column("bread_id", ForeignKey("bread.id"), primary_key=True),
)


class Baker(Base):
    __tablename__ = "baker"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    pronouns = Column(String)
    contact = relationship("ContactInfo", uselist=False, back_populates="baker")
    specialties = relationship(
        "Bread", secondary=baker_specialty, back_populates="specializing_bakers"
    )

    def __repr__(self):
        return f"<Baker {self.name} ({self.pronouns})>"


class Bread(Base):
    __tablename__ = "bread"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_delicious = Column(Boolean)
    ingredient_cost = Column(Numeric)
    specializing_bakers = relationship(
        "Baker", secondary=baker_specialty, back_populates="specialties"
    )

    def __repr__(self):
        return f"<Bread {self.name}>"


def create_all(engine):
    Base.metadata.create_all(engine)
