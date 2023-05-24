from sqlalchemy import DateTime, Integer, MetaData, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Session, mapped_column

from settings import settings

engine = create_engine(settings.db_url)
metadata_obj = MetaData()
metadata_obj.create_all(engine)


class Base(DeclarativeBase):
    pass


class IDModel(Base):
    __abstract__ = True

    id = mapped_column(Integer, primary_key=True)


class TimeStampedModel(IDModel):
    __abstract__ = True

    created = mapped_column(DateTime, default=func.now())
    updated = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class QuizQuestion(TimeStampedModel):
    __tablename__ = "quiz_question"

    question = mapped_column(String, nullable=False, unique=True)
    external_id = mapped_column(Integer, nullable=False)
    answer = mapped_column(String, nullable=False)


async def get_db():
    return Session(engine)


Base.metadata.create_all(engine)
