# Project
## Goals
Fully featured character generator, both random and user driven, supporting basic and
advanced features. Able to randomize any choices the user doesn't want to make, from
bonds, to backstory, to stats. Saves everything in a MongoDB database, and has a 
responsive interface in Angular. 

I want this personally, because I think it would be cool to have this for Delta Green. 
I want to program this publicly because I think it will be a good way to show off what
I'm capable of in python to prospective future employers. 

And I want to give back to the RPG community. I spent countless hours playing with 
[PCGEN](http://pcgen.org/) when I was younger. I don't know Java, so I can't really contribute to 
PCGEN. But I can try and make something of my own and make sure it's FOSS. Since I'm currently 
obsessed with Delta Green and there appears to be no Delta Green character generator, here's where I
can make a big impact. 

It also helps that Delta Green is under the OGL. I can enforce a separation between OGL content and
non-OGL using my .gitignore file. If/when I end up hosting this, I hope to use a password from the
Delta Green sourcebook to gatekeep non-OGL content to only people who have bought the book. 

# Phase 1

## Goals
* Random generation of a complete Delta Green character (stats, bonds, disorders, etc.)
* Front end that displays a random character every time the endpoint is visited
* Characters are saved in a database in a sensible format
* Open gaming license vs not distinction made in DB and on front end and players must check
if they own the actual game and can access the non open-gaming license content (hopefully this is
legal?)

## Implementation Journal
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
* I've now found out that there can be enumerated sub-skills in the choices a class can make, 
although this won't affect any open classes - it's only for the closed classes.
    * I'm going to try and come up with a system that sometimes picks sub-skills based on their
    relative abundance IFF sub-skills exist for the choices for that class
* After this, I think my top priorities are:
    * Creating a bonds json file, putting bonds in the database, logic for applying them to 
    characters
        * This will probably require some layout and query logic such that professors with the 
        criminal package don't get a war buddy bond. 
    * Double checking my logic in the Character Class and possibly simplifying it
    * Documenting Character.py and Generator.py
    * Unit tests for Character.py and Generator.py
* That set of priorities is now complete. I've also managed to polish off both disorders and 
damaged veterans, the last things keeping this from being feature complete
* The two most urgent next steps are:
    * Differentiating OGL and non-OGL content in the database
    * Saving and loading characters
* Both of those priorities completed on 2017/09/04. 
    * Next up is a plan for APIs, then developing those APIs using Flask