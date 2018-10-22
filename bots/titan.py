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
import subprocess
import re
from pathlib import Path

client = discord.Client()

name = "titan"
procs = {}

@client.event
@asyncio.coroutine
def on_ready():
	print("Logged in as " + client.user.name)

def update():
	ret = subprocess.check_output("git pull -q".split(" ")).decode("utf-8")

	if ret == "":
		return "Was already up to date"
	else:
		return "Updated repository"

def startBot(botname):
	global procs
	if botname in procs:
		return "{0} already running. Use `poll` to see if it died.".format(botname)
	p = subprocess.Popen(["./startbot", botname])
	procs[botname] = p
	return "Started {0}".format(botname)

def pollProcs():
	global procs
	i = 0
	bots = list(procs.keys())
	for bot in bots:
		if procs[bot].poll is not None:
			del procs[bot]
		else:
			i += 1
@client.event
@asyncio.coroutine
def on_message(message):
	if message.author.bot or len([role for role in message.author.roles if str(role) == "Bot Control"]) == 0:
		return
	if message.content.startswith(name):
		args = message.content.split(" ")
		if len(args) < 2:
			return
		if args[1] == "die":
			yield from client.logout()
		elif args[1] == "help":
			yield from client.send_message(message.channel, "Available commands: update, start bot_name [bot_name ...], poll, die")
		elif args[1] == "update":
			yield from client.send_message(message.channel, update())
		elif args[1] == "start":
			for bot in args[2:]:
				if re.search("[^a-zA-Z]", bot):
					yield from client.send_message(message.channel, "Illegal bot name")
				else:
					yield from client.send_message(message.channel, startBot(bot))
		elif args[1] == "poll":
			pollProcs()
			yield from client.send_message(message.channel, "Done")

file = open("tokens/" + name + ".token", "r")
token = file.read()
file.close()
client.run(token)
