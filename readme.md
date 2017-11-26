# Delta Green Character Generator
Open Source [Delta Green](http://www.delta-green.com/) random character generator.

## Features
* Generates a complete Delta Green character (all skills, stats, derived attributes, bonds, one 
third of characters are damaged veterans)

## Installing
* Install Python 3.5
* Create a virtual environment in the project folder with `virtualenv -p python3 venv`
* Activate the virtual environment with `source venv/bin/activate`
* Install the necessary packages with `pip install requirements.txt`
* You'll need to create a MongoDB database and save the connection string and database name to a
file called `ExternalServices.py` (in the top level project directory). This file will need the 
globals `DATABASE` (the name of the mongo database you plan to use) and `MONGO_STRING` 
(the connection string you intend to use). An example file has been provided as 
`ExternalServicesExample.py`
* Add the open gaming content to your Mongo database with `python SeedDB.py OpenGamingJSON/`
* Whenever you open this in a new terminal/powershell window, you'll have to activate the VENV again
with `source venv/bin/activate`

## Using (Command Line)
* From the top level directory: `python Test.py`
    * The results will print to the console.

## Using (Web)
* With venv activated, run `python server.py` in the top level folder
    * You can generate a character by navigating to `http://localhost:8080/api/v1/characters` in
    your favourite web browser
    * For now, the character is just a JSON object

## Running The Tests
From the top level directory: `python -m unittest Tests/test_*`

## Building The Docs
From the `Docs` directory, run `make html`. 

## Wishlist
* Language families/association scores to give more realistic language combinations
* When picking a random skill in a package, more weight given to existing skills
* Classes provide some bias to the stats
* More open source skill packages and classes

## Helping Out
* The best way to help out right now is probably submitting homebrew skill packages or classes.
These are just JSON files that can be edited in a text editor, even without programming experience.

## Legal
Parts of Delta Green are licensed under the OGL. I'm trying to only publicly share the parts that
are. If you are a rights holder or (heavens forfend) their lawyer, you can reach me at 
zejacobi (squiggly a/at character thingy) gmail (dot) com