# ChatBot

This repository contains the source files for some Discord bots. The source
code is available under the MIT License, copyright Matthew Chen and Arc676/Alessandro Vinciguerra.

Io
- Named after one of Jupiter's moons
- Has basic chatbot capabilities
- Recognizes when it is addressed and reacts to predetermined commands
- Replies to movie quotes

Nix
- Named after one of Pluto's moons
- Plays Number Guess with any number of players (as the player with the number)
- User can specify bounds

Styx
- Named after one of Pluto's moons
- Plays Number Guess with any number of players (as the guesser)
- Can play against Nix

Titania
- Named after one of Uranus' moons
- Searches for Magic: the Gathering cards 

Janus
- Named after one of Saturn's moons
- Parses messages for options and picks a random one
- Manages polls on which users can vote

Pluto
- Named after a dwarf planet in our solar system (as of 2006)
- Asks random questions from the set of questions in Cards Against Humanity
- Pairs with Charon

Charon
- Named after one of Pluto's moons
- Answers questions with random answers from Cards Against Humanity
- Pairs with Pluto

System Requirements:
[Node.js](http://nodejs.org)

## Instructions for running:
The directory containing the bots must look like this (assuming you don't modify the scripts).
```
/path/to/dir
|-bots
|-tokens
```
Use the `startbot` script to run the bots *while you are in the directory* i.e. `./startbot botname`.
The script will run `node` with the specified script in the background.

The bots folder contains the bot scripts.

The tokens folder contains files named `botname.token` containing the secret token of the app with
**NO TRAILING NEWLINE**. These tokens are not included in this repository (because then you could
impersonate our bots).
