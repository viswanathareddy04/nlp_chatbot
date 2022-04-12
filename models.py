from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

sqlite_db = {'drivername': 'sqlite', 'database': 'db.sqlite'}

engine = create_engine(URL(**sqlite_db), echo=True)

Base = declarative_base()

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    roll_no = Column(String)
    name = Column(String)
    age = Column(Integer)
    fee = Column(Integer)
    exam = Column(String)
    grades = relationship("Grade", backref="student")


class Subject(Base):
    __tablename__ = "subject"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    grades = relationship("Grade", backref="subject")


class Grade(Base):
    __tablename__ = "grade"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    mark = Column(Integer)


class TimeTable(Base):
    __tablename__ = "timetable"

    weekday = Column(String, primary_key=True)
    description = Column(String)


class TrainingData(Base):
    __tablename__ = "training_data"

    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    sample = Column(String)


class IntentResponse(Base):
    __tablename__ = "intent_response"

    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    intent = Column(String)
    response = Column(String)


Base.metadata.create_all(bind=engine)
