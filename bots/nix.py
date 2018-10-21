# MIT License

# Copyright (c) 2017-8 Arc676/Alessandro Vinciguerra

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import discord
import asyncio
from random import randint

client = discord.Client()

name = "nix"
answers = {}

@client.event
@asyncio.coroutine
def on_ready():
	print("Logged in as " + client.user.name)

@asyncio.coroutine
def replyToMsg(msgObj, msg):
	global client
	yield from client.send_message(msgObj.channel, "{0} {1}".format(msgObj.author.mention, msg))

@client.event
@asyncio.coroutine
def on_message(message):
	if message.content.startswith(name + " "):
		if message.content.endswith(" die"):
			yield from client.logout()
		elif message.content.endswith(" about"): 
			yield from replyToMsg(message, "Hi! My name is Nix, one of the moons of Pluto! Unlike Charon, I was discovered recently along with Kerberos, Hydra, and my fellow bot Styx. I'm named after the Greek embodiment of night and darkness, but the spelling was changed so I would not be confused for an asteroid named Nyx.")
		elif "newgame" in message.content:
			args = message.content.split(" ")
			if len(args) != 4:
				yield from replyToMsg(message, "Usage: nix newgame lowBound upBound")
			try:
				lowerBound = int(args[2])
				upperBound = int(args[3])
				answers[message.author] = randint(lowerBound, upperBound)
				yield from replyToMsg(message, "Alright, let's play!")
			except ValueError:
				yield from replyToMsg(message, "Failed to parse arguments")
		elif message.author in answers:
			try:
				guess = int(message.content[len(name) + 1:])
				if guess == answers[message.author]:
					del answers[message.author]
					yield from replyToMsg(message, "Correct!")
				elif guess < answers[message.author]:
					yield from replyToMsg(message, "Too low!")
				else:
					yield from replyToMsg(message, "Too high!")
			except ValueError:
				yield from replyToMsg(message, "Failed to parse guess")

file = open("tokens/" + name + ".token", "r")
token = file.read()
file.close()
client.run(token)
