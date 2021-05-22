"""
This module defines an example model that can be used with SQLAlchemy to initialize
a database.
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import registry, relationship
from sqlalchemy.sql.schema import Index, Table
from sqlalchemy.sql.sqltypes import Integer

mapper_registry = registry()
metadata = mapper_registry.metadata

Base = mapper_registry.generate_base()


# region mixins


class ETagMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    etag = Column(String(50), nullable=False)


ETagMixin.created_at._creation_order = 9000
ETagMixin.updated_at._creation_order = 9001
ETagMixin.etag._creation_order = 9002


# endregion


country_topic_table = Table(
    "topic_country",
    Base.metadata,
    Column("country_id", String(2), ForeignKey("country.id"), primary_key=True),
    Column("topic_id", Integer, ForeignKey("topic.id"), primary_key=True),
)


class Country(Base):
    __tablename__ = "country"
    id = Column(String(2), primary_key=True)
    name = Column(String(100))

    topics = relationship(
        "Topic", secondary=country_topic_table, back_populates="countries"
    )

    def __repr__(self):
        return f"Country(id={self.id!r}, name={self.name!r})"


class Topic(ETagMixin, Base):
    __tablename__ = "topic"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    description = Column(String)

    countries = relationship(
        "Country", secondary=country_topic_table, back_populates="topics"
    )

    def __repr__(self):
        return f"Topic(id={self.id!r}, name={self.name!r})"


Index("ix_topic_country_topic_id", "topic_country.topic_id")
Index("ix_topic_country_country_id", "topic_country.country_id")
