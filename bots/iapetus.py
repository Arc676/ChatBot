# MIT License

# Copyright (c) 2018 Arc676/Alessandro Vinciguerra

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
import datetime

client = discord.Client()

name = "iapetus"
dates = {}

@client.event
@asyncio.coroutine
def on_ready():
	print("Logged in as " + client.user.name)

@asyncio.coroutine
def replyToMsg(msgObj, msg):
	global client
	yield from client.send_message(msgObj.channel, "{0} {1}".format(msgObj.author.mention, msg))

def daysUntil(date):
	return (date - datetime.date.today()).days

@client.event
@asyncio.coroutine
def on_message(message):
	if message.author.bot:
		return
	if message.content.startswith(name):
		args = message.content.split(" ")
		if len(args) < 2:
			return
		if args[1] == "die":
			yield from client.logout()
		elif args[1] == "help":
			yield from client.send_message(message.channel, "Available commands: countdown event_name YYYY-MM-DD, list, die, help, about")
		elif args[1] == "about":
			yield from client.send_message(message.channel, "Iapetus is believed to be the Greek God of mortality. I share this name with one of Saturn's moons because my function is to provide a countdown to the inevitable.")
		elif args[1] == "countdown":
			if len(args) < 4:
				return
			try:
				components = [int(c) for c in args[3].split("-")]
				date = datetime.date(components[0], components[1], components[2])
				if message.author not in dates:
					dates[message.author] = []
				dates[message.author].append({
					"name" : args[2],
					"date" : date
				})
				yield from replyToMsg(message, "Added countdown for {0}. Only {1} day(s) to go!".format(args[2], daysUntil(date)))
			except:
				yield from replyToMsg(message, "The provided date was invalid")
		elif args[1] == "list":
			resp = "Your countdowns:"
			for event in dates[message.author]:
				resp += "Days until {0}: {1}\n".format(event["name"], daysUntil(event["date"]))
			yield from replyToMsg(message, resp.rstrip())

file = open("tokens/" + name + ".token", "r")
token = file.read()
file.close()
client.run(token)
