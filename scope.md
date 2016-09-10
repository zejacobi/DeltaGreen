# Project
## Goals
Fully featured character generator, both random and user driven, supporting basic and
advanced features. Able to randomize any choices the user doesn't want to make, from
bonds, to backstory, to stats. Saves everything in a MongoDB database, and has a 
responsive interface in Angular. 

I want this personally, because I think it would be cool to have this for Delta Green. 
I want to program this publicly because I think it will be a good way to show off what
I'm capable of in python to prospective future employers.

# Phase 1

## Goals
* Random generation of a complete Delta Green character (stats, bonds, disorders, etc.)
* Front end that displays a random character every time the endpoint is visited
* Characters are saved in a database in a sensible format
* Open gaming license vs not distinction made in DB and on front end and players must check
if they own the actual game and can access the non open-gaming license content (hopefully this is
legal?)

## Implementation 
* Classes for connecting to Mongo Database
    * Wrapper class/function for making requests async
        * Should this just be the default for all Mongo Requests?
        * This might get annoying if I use a variety of query types, to have to wrap 
        each one
        * Can I use decorators?
        * I should use the queue module with one queue for this?
            * Probably not queue, because that's for doing everything in a bunch of threads then
            unblocking at the end
    * Final solution will probably use a class that wraps threads around a function, uses the
    [splat operator] [1] (`*`), and a class for Mongo connections to a certain database.


[1]: http://stackoverflow.com/questions/4979542/python-use-list-as-function-parameters 