# Discord Bots

This repository contains the source files for some Discord bots. The source code is available under the MIT License, copyright Matthew Chen and Arc676/Alessandro Vinciguerra.

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

Deimos
- Named after one of Mars' moons
- Reads [Vongsprache](https://github.com/Arc676/Vongsprache) scripts, evaluates them, and replies with the output
- Requires a `vongsprache` executable in the project root
- Requests should contain two code blocks, the first of which contains the script and the second of which contains any user input to be passed to the script

Prometheus
- Named after an inner satellite of Saturn
- Generates calendar "facts" from the xkcd comic 1930

Titan
- Control bot
- Can start other bots and and run `git pull` to update the local scripts if a bot needs to be updated
- Named after Saturn's biggest moon

Iapetus
- Named after one of Saturn's moons
- Provides a countdown service by determining the number of days to a given date

Hyperion
- Named after one of Saturn's moons
- Converts between Morse code and normal text

## System Requirements:

Python 3.4 or later. See the requirements for [the Discord API](https://github.com/Rapptz/discord.py) and the [MTG SDK](https://github.com/MagicTheGathering/mtg-sdk-python) for more details on required Python packages.

## Included scripts and utilities

The directory containing the bots must look like this (assuming you don't modify the scripts).
```
/path/to/dir
|-bots
|-tokens
```
Use the `startbot` script to run the bots *while you are in the directory* i.e. `./startbot botname`.
The script will run `python3` with the specified script in the background.

The bots folder contains the bot scripts.

The tokens folder contains files named `botname.token` containing the secret token of the app with **NO TRAILING NEWLINE**. These tokens are not included in this repository (because then you could impersonate our bots).

The `restartbots` script checks if any bots have died and restarts them. This can be added to a cron job to ensure maximum uptime in case any bots die due to unexpectedly terminated connections.

## Legal

The bots are available under the MIT license. The text for Cards Against Humanity (in `CAH/`) is available under [CC-BY-NC-SA 2.0](https://creativecommons.org/licenses/by-nc-sa/2.0/). See [the official website](https://www.cardsagainsthumanity.com) for more details.

The images of the celestial bodies come from Wikipedia. All images are in the public domain as they were created by NASA.
