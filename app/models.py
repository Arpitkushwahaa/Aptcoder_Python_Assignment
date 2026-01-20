from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()


class Student(Base):
    """Student model"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    grade = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    enrollments = relationship("Enrollment", back_populates="student")


class Course(Base):
    """Course model"""
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    
    enrollments = relationship("Enrollment", back_populates="course")


class Enrollment(Base):
    """Enrollment model"""
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


class QueryLog(Base):
    """Query log model for analytics"""
    __tablename__ = "query_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    generated_sql = Column(String, nullable=False)
    execution_time = Column(Integer, nullable=False)  # milliseconds
    created_at = Column(DateTime, default=datetime.utcnow)
