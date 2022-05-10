import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'                #table name

    # table fields are created here
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class MenuItem(Base):
    __tablename__ = 'menu_item'                 #table name

    #table fields are created here
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))  #foreign key used to link two tables
    restaurant = relationship(Restaurant)           #foreingKey link association with related table

    # We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }


if __name__ == "__main__":
    # create the db file
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.create_all(engine)