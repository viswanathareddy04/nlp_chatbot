from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
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


Base.metadata.create_all(bind=engine)
