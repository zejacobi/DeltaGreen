# Delta Green Character Generator
Open Source [Delta Green] [1] random character generator.

## Features

## Installing
* Create a virtual environment in the project folder with `virtualenv -p python3 venv`
* Activate the virtual environment with `source venv/bin/activate`
* Install the necessary packages with `pip install requirements.txt`
* You'll need to create a MongoDB database and save the connection string and database name to a
file called `ExternalServices.py` (in the top level project directory). This file will need the 
globals `DATABASE` and `MONGO_STRING`
* Add the open gaming content to your Mongo database with `python SeedDB.py OpenGamingJSON/`

## Running The Tests


[1]: http://www.delta-green.com/