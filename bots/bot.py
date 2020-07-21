# MIT License

# Copyright (c) 2018-9 Arc676/Alessandro Vinciguerra

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
	"""Signal handler for SIGTERM
	"""
	asyncio.ensure_future(instance.logout()).__await__()

class CelestialBot(discord.Client):
	def __init__(self, name, color=0xFFFF):
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
		self.color = color
		self.help = discord.Embed(title="Commands available for {0}".format(name), color=self.color)
		self.help.add_field(name="help", value="Shows this help message", inline=False)
		self.help.add_field(name="about", value="Shows information about {0}".format(name), inline=False)
		self.about = "No bot description available"
		self.allowBotControl = False
		self.defaultCmd = None
		self.handleEverything = False
		self.commands = {
			"die" : self.killBot,
			"thanks" : self.youreWelcome,
			"help" : self.showHelp,
			"about" : self.showAbout
		}

	async def showHelp(self, message, args):
		"""Replies to a given message with the help block for this bot

		Args:
			message: Message to which to reply
			args: Content of the message split by whitespace
		"""
		await self.reply(message, embed=self.help)

	async def youreWelcome(self, message, args):
		"""Replies with 'You're welcome'

		Args:
			message: Message to which to reply
			args: Content of the message split by whitespace
		"""
		await self.reply(message, "You're welcome!", reply=True)

	async def showAbout(self, message, args):
		"""Replies to a given message with the about message for this bot

		Args:
			message: Message to which to reply
			args: Content of the message split by whitespace
		"""
		await self.reply(message, self.about)

	async def killBot(self, message, args):
		"""Disconnects the bot if the author of the kill message is authorized to request this

		Args:
			message: Message object
			args: Message content split by whitespace
		"""
		if self.isBotController(message.author) and (not self.handleEverything or self.wasAddressed(message)):
			await self.logout()

	def isBotController(self, author):
		"""Determine whether a user is an authorized bot controller

		Args:
			author: User to check

		Returns:
			Whether the user's ID is in the bot controllers file
		"""
		file = open(".botcontrollers", "r")
		isController = str(author.id) in [line.strip() for line in file.readlines()]
		file.close()
		return isController

	def wasAddressed(self, message):
		"""Determine whether the bot was addressed in a given message

		Return:
			Whether the bot was addressed
		"""
		return message.content != "" and (message.content.split()[0].lower().strip() == self.name.lower() or self.user in message.mentions)

	def getToken(self):
		"""Obtain Discord token for the bot

		Return:
			Discord token as text
		"""
		file = open("tokens/" + self.name.lower() + ".token", "r")
		token = file.read()
		file.close()
		return token

	def buildHelp(self, cmds):
		"""Builds a help block for the bot given a dictionary of commands and descriptions

		Args:
			cmds: {command : description} dictionary of the available commands
		"""
		for cmd, desc in cmds.items():
			self.help.add_field(name=cmd, value=desc, inline=False)

	def getHandler(self, message, args):
		"""Gets the appropriate handler for a given message

		Args:
			message: Incoming message
			args: Message content split by whitespace

		Return:
			The handler function for the incoming message, if any
		"""
		if message.author.bot and not self.allowBotControl:
			return None
		if self.wasAddressed(message):
			if len(args) >= 2 and args[1] in self.commands:
				return self.commands[args[1]]
			return self.defaultCmd
		elif self.handleEverything:
			return self.defaultCmd

	async def reply(self, msgObj, msg='\u200b', embed=None, reply=False):
		"""Replies to a message

		Args:
			msgObj: Message object to which to reply
			msg: Message content for reply (defaults to zero width space)
			embed: The embed object to include in the reply (defaults to None)
			reply: Whether the reply should ping the author of the orginal message (defaults to False)
		"""
		await msgObj.channel.send("{0} {1}".format(msgObj.author.mention if reply else "", msg).strip(), embed=embed)

	async def on_ready(self):
		"""After login
		"""
		print("Logged in as " + self.user.name)

	async def on_message(self, message):
		"""Message handler

		Args:
			message: Incoming message
		"""
		args = message.content.split()
		handler = self.getHandler(message, args)
		if handler is not None:
			await handler(message, args)
