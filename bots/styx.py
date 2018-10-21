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

client = discord.Client()

name = "styx"

opponent = {}
delta = {}
guess = {}
bounds = {}

@client.event
@asyncio.coroutine
def on_ready():
	print("Logged in as " + client.user.name)

@asyncio.coroutine
def computeGuess(channel, user, wasHigh):
	global opponent
	global delta
	global guess
	global bounds
	if guess[user] >= bounds[user][1] or guess[user] <= bounds[user][0]:
		channel.send(opponent[user] + ", you've been giving me contradictory information")
		return
	if wasHigh:
		bounds[user][1] = guess[user]
		guess[user] -= delta[user]
	else:
		bounds[user][0] = guess[user]
		guess[user] += delta[user]
	if delta[user] > 1:
		delta[user] //= 2
	yield from sendGuess(channel, user)

@asyncio.coroutine
def sendGuess(channel, user):
	global opponent
	global guess
	yield from client.send_message(channel, "{0} {1}".format(opponent[user], int(guess[user])))

@asyncio.coroutine
def replyToMsg(msgObj, msg):
	global client
	yield from client.send_message(msgObj.channel, "{0} {1}".format(msgObj.author.mention, msg))

@client.event
@asyncio.coroutine
def on_message(message):
	if client.user in message.mentions:
		user = message.author
		if message.content.endswith("die"):
			yield from client.logout()
		elif message.content.endswith(" about"):
			yield from replyToMsg(message, "Hi, I'm Styx! I'm one of the smaller moons of Pluto. I'm so small that I'm more of an oblong potato than a sphere! I'm named after the river in the Greek underworld that made Achilles invulnerable - except for his heel of course.")
		elif " play " in message.content:
			args = message.content.split(" ")
			if len(args) < 5:
				yield from replyToMsg(message, "Usage: @styx play username lowBound upBound [verbose]")
			if user.name != args[2]:
				for member in message.server.members:
					if member.name.upper() == args[2].upper():
						user = member
						break
			try:
				low = int(args[3])
				high = int(args[4])
				opponent[user] = args[2]
				if len(args) > 5 and args[5] == "verbose":
					yield from client.send_message(message.channel, "{0} newgame {1} {2}".format(opponent[user], low, high))
				guess[user] = (high - low) / 2 + low
				delta[user] = guess[user] // 2
				bounds[user] = [low, high]
				yield from sendGuess(message.channel, user)
			except ValueError:
				yield from replyToMsg(message, "Failed to parse values")
		elif user in guess:
			if "low" in message.content:
				yield from computeGuess(message.channel, user, False)
			elif "high" in message.content:
				yield from computeGuess(message.channel, user, True)
			elif "Correct" in message.content:
				del delta[user]
				del guess[user]
				yield from replyToMsg(message, "Yay!")

file = open("tokens/" + name + ".token", "r")
token = file.read()
file.close()
client.run(token)
