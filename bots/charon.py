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
import re
from random import randint

client = discord.Client()

name = "charon"

allAnswers = []
aCount = 0

@client.event
@asyncio.coroutine
def on_ready():
	global aCount
	global allAnswers
	print("Logged in as " + client.user.name)
	file = open("CAH/answers.txt", "r")
	allAnswers = file.readlines()
	file.close()
	aCount = len(allAnswers) - 1

def getRandomAnswer():
	global aCount
	global allAnswers
	return re.sub("([\*_])", r"\\\1", allAnswers[randint(0, aCount)])

@client.event
@asyncio.coroutine
def on_message(message):
	if message.content.startswith(name):
		if message.content.endswith("die"):
			yield from client.logout()
		else:
			parts = message.content.split(" ")
			times = 1
			if len(parts) > 1:
				try:
					times = int(parts[1])
				except:
					pass
			answer = ""
			for i in range(times):
				answer += getRandomAnswer()
			yield from client.send_message(message.channel, "{0} {1}".format(message.author.mention, answer.rstrip()))

file = open("tokens/" + name + ".token", "r")
token = file.read()
file.close()
client.run(token)
