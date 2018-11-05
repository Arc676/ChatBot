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
import sys
import signal

instance = None

def signal_handler(sig, frame):
	asyncio.ensure_future(instance.logout()).__await__()

class CelestialBot(discord.Client):
	def __init__(self, name):
		"""Initializes a new bot

		Args:
			name: Bot name
		"""
		# token control and base class control
		super().__init__()

		global instance
		instance = self
		signal.signal(signal.SIGTERM, signal_handler)

		# bot properties
		self.name = name
		self.allowBotControl = False
		self.defaultCmd = None
		self.handleEverything = False
		self.commands = {
			"die" : self.killBot
		}

	@asyncio.coroutine
	def killBot(self, message, args):
		if self.isBotController(message.author) and (not self.handleEverything or self.wasAddressed(message)):
			yield from self.logout()

	def isBotController(self, author):
		return "Bot Control" in [str(role) for role in author.roles]

	def wasAddressed(self, message):
		return message.content != "" and (message.content.split(" ")[0].lower().strip() == self.name.lower() or self.user in message.mentions)

	def getToken(self):
		file = open("tokens/" + self.name.lower() + ".token", "r")
		token = file.read()
		file.close()
		return token

	@asyncio.coroutine
	def replyToMsg(self, msgObj, msg):
		yield from self.send_message(msgObj.channel, "{0} {1}".format(msgObj.author.mention, msg))

	@asyncio.coroutine
	def on_ready(self):
		print("Logged in as " + self.user.name)

	@asyncio.coroutine
	def on_message(self, message):
		if message.author.bot and not self.allowBotControl:
			return
		args = message.content.split(" ")
		if self.wasAddressed(message):
			if len(args) >= 2 and args[1] in self.commands:
				yield from self.commands[args[1]](message, args)
			elif self.defaultCmd is not None:
				yield from self.defaultCmd(message, args)
		elif self.handleEverything and self.defaultCmd is not None:
			yield from self.defaultCmd(message, args)
