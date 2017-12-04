[![codecov](https://codecov.io/gh/zejacobi/DeltaGreen/branch/master/graph/badge.svg)](https://codecov.io/gh/zejacobi/DeltaGreen)
[![Build Status](https://travis-ci.org/zejacobi/DeltaGreen.svg?branch=master)](https://travis-ci.org/zejacobi/DeltaGreen)

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
From the top level directory: `python tests.py`

Remember to add all new tests to the `tests.py` file.

To run the unit tests with coverage, run
```bash
coverage run tests.py
coverage report
```

*Note:* If a `ExternalServices.py` file has not been created by the time you run the unit tests,
it will automatically create one for you. This is a semi-accidental result of needing that file
to exist for the tests to run. 

## Building The Docs
From the `Docs` directory, run `make html`. 
Sometimes the API autodocs stop tracking changes and the whole _build directory has to be deleted
to remind them to build what they should. If this happens, you can run (with an activated venv) the
script `make_docs.sh` (*nix only) in the `Docs` directory to handle deleting the _build folder
automatically before building the updated docs.

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