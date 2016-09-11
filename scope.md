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
    * Final solution will probably use Mongo and use threads and queues only when necessary for 
    multiple requests. 
        * If I want smart context switching when things are idle on I/O, threading actually needs to
        go higher up. 
* Open Gaming License content created
    * Default skills in an object
    * More can wait until I have some arch done
* Class for all the key components of a character
* Generate all of the skills for a character using a set of recursive functions that dynamically
generate sub-skills when they're required
    * By a sub-skill, I mean Craft (Microelectronics) and its ilk
    * I want these to be editable separate of the main skill list, to avoid filling the list of 
    skills up with these, like D&D 3.5e character generators would
* Similar functions should allow me to add 20 to each skill for apply a package
* Once all skills are assigned, pick the top five. Using a separate dictionary that applies a stat
to each skill, then determine what order to put skills in.
    * Skills can use multiple stats and we count the totals
    * Power gets 2 free points (willpower, san)
    * Str gets 0.5 free points (HP)
    * Con gets 0.5 free points (HP)