# Delta Green Character Generator
Open Source [Delta Green] [1] random character generator.

## Features
* Generates a complete Delta Green character (all skills, stats, derived attributes, bonds)
    * Can't yet do damaged veterans

## Installing
* Create a virtual environment in the project folder with `virtualenv -p python3 venv`
* Activate the virtual environment with `source venv/bin/activate`
* Install the necessary packages with `pip install requirements.txt`
* You'll need to create a MongoDB database and save the connection string and database name to a
file called `ExternalServices.py` (in the top level project directory). This file will need the 
globals `DATABASE` and `MONGO_STRING`
* Add the open gaming content to your Mongo database with `python SeedDB.py OpenGamingJSON/`

## Using
* From the top level directory: `python Test.py`
    * The results will print to the console.

## Running The Tests
* Forthcoming

## Wishlist
* Language families/association scores to give more realistic language combinations
* When picking a random skill in a package, more weight given to existing skills
* Classes provide some bias to the stats

## Legal
Parts of Delta Green are licensed under the OGL. I'm trying to only publicly share the parts that
are. If you are a rights holder or (heavens forfend) their lawyer, you can reach me at 
zejacobi (squiggly a/at character thingy) gmail (dot) com


[1]: http://www.delta-green.com/