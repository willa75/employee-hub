import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Company(Base):
    __tablename__ = 'company'
    name = Column(
        String(80), nullable = False)
    id = Column(
        Integer, primary_key = True)

class Employee(Base):
    __tablename__ = 'employee'
    firstname = Column(String(80), nullable = False)
    lastname = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    zipcode = Column(Integer)
    birthday = Column(Integer)
    birthmonth = Column(Integer)
    birthyear = Column(Integer)
    company_id = Column(
        Integer, ForeignKey('company.id'))
    company = relationship(Company)

# Added this serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):

        return {
            'name': self.firstname,
            'lastname': self.lastname,
            'id': self.id,
            'zipcode': self.zipcode,
            'birthday': self.birthday,
            'birthmonth': self.birthmonth,
            'birthyear': self.birthyear,
        }

engine = create_engine('sqlite:///companyemployees.db')

Base.metadata.create_all(engine)