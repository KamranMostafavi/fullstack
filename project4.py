from flask import Flask

# needed to access the ORM
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# needed to access the objects needed to access the tables
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)


def getOrmSession():
    engine = create_engine(
        'sqlite:///restaurantmenu.db')  # indicate dbase file to use and create an object for
    Base.metadata.bind = engine  # bind the base model to the engine (maps class definitions to corresponding tables in db file)
    DBSession = sessionmaker(
        bind=engine)  # session contains work to be done by the engine prior to committing.
    session = DBSession()  # an instance of the DBSession creates a staging session to create db commands.
    return session



@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    #create ORM session to database file
    session = getOrmSession()
    # get all the items in MenuItem database whose restaurant_id matches the restuarant_id passed in url
    items=session.query(MenuItem).filter_by(restaurant_id=restaurant_id)

    output=''
    for item in items:
        output += item.name + '<br>'
        output += item.price + '<br>'
        output += item.description + '<br><br>'

    return output      #this is the output of the GET call that is displaced by client browser.

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)