from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# need to have run database_setup.py already to create the restaurantmenu.db file
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')  #indicate dbase file to use and create an object for
Base.metadata.bind = engine    #bind the base model to the engine (maps class definitions to corresponding tables in db file)
DBSession = sessionmaker (bind = engine)    #session contains work to be done by the engine prior to committing.
session = DBSession()   # an instance of the DBSession creates a staging session to create db commands.

#create a new restaurant in the database
myFirstRestaurant = Restaurant(name='Pizza Palace')
session.add (myFirstRestaurant)   #add myFirstRestuarant to the staging zone
session.commit()                  #commit so it is writtent the database file

cheesepizza = MenuItem(name='Cheese Pizza', description = 'made by all natural ingredients', course = 'Entree',
                       price = '$8.99', restaurant = myFirstRestaurant)
session.add (cheesepizza)
session.commit()

# display contents of the Restaurant table
for row in session.query(Restaurant).all():
    print (row.name, row.id)

# display contents of the MenuItem table
for row in session.query(MenuItem).all():
    print (row.name, row.description, row.course, row.price, row.restaurant_id, row.restaurant.name)


