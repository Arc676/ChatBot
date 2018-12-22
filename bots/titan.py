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

from bot import CelestialBot
import asyncio
import subprocess
import re
from pathlib import Path
import sqlite3

class Titan(CelestialBot):
	def __init__(self):
		super().__init__("Titan", color=0xD3C171)
		self.buildHelp({
			"start | kill | restart botname [botname ...]" : "Starts, terminates, or restarts the given bot(s); bot names cannot contain spaces",
			"register | unregister userID" : "(Un)registers the user with the given ID as a bot controller; only bot controllers can use Titan's functions",
			"list" : "Shows a list of all running bots and their PIDs"
		})
		self.about = "I'm Titan, named after the largest of Saturn's moons. In Greek mythology, the Titans were a race of powerful deities"
		self.commands.update({
			"register" : self.registerController,
			"unregister" : self.unregisterController,
			"update" : self.updateRepo,
			"start" : self.launchBot,
			"restart" : self.restart,
			"kill" : self.kill,
			"list" : self.listBots
		})
		self.db = sqlite3.connect("titan.db")
		self.dbc = self.db.cursor()
		try:
			self.dbc.execute("CREATE TABLE procs (botname text, pid INTEGER)")
		except sqlite3.OperationalError:
			pass

	async def updateRepo(self, message, args):
		"""Attempts to update the local git repository

		Args:
			message: Message object
			args: Message content split by whitespace
		"""
		await self.reply(message, self.update())

	async def launchBot(self, message, args):
		"""Attempts to launch a bot

		Args:
			message: Message object
			args: Message content split by whitespace
		"""
		for bot in args[2:]:
			if self.isValidBotName(bot):
				await self.reply(message, self.startBot(bot))
			else:
				await self.reply(message, "Illegal bot name")
		self.db.commit()

	async def kill(self, message, args):
		"""Attempts to terminate a bot

		Args:
			message: Message object
			args: Message content split by whitespace
		"""
		for bot in args[2:]:
			await self.reply(message, self.terminateBot(bot))
		self.pollProcs()
		self.db.commit()

	async def restart(self, message, args):
		"""Attempts to restart a bot

		Args:
			message: Message object
			args: Message content split by whitespace
		"""
		for bot in args[2:]:
			if self.isValidBotName(bot):
				resp = self.terminateBot(bot) + "\n"
				resp += self.startBot(bot)
				await self.reply(message, resp)
			else:
				await self.reply(message, "Illegal bot name")

	async def listBots(self, message, args):
		"""Lists all bots whose PIDs are being tracked

		Args:
			message: Message object
			args: Message content split by whitespace
		"""
		self.pollProcs()
		resp = "Running bots:\n{0}".format(
			"\n".join([(lambda x: "Name: {0}, PID: {1}".format(x[0], x[1]))(tuple(record))
				for record in self.dbc.execute("SELECT * FROM procs")])
		)
		await self.reply(message, resp)

	async def registerController(self, message, args):
		"""Registers a new bot controller in the bot controller file

		Args:
			message: Message object
			args: Message content split by whitespace
		"""
		file = open(".botcontrollers", "a")
		file.write("\n{0}".format(args[2]))
		file.close()
		await self.reply(message, "Registered user ID {0} as bot controller".format(args[2]))

	async def unregisterController(self, message, args):
		"""Removes a given user from the bot controller file

		Args:
			message: Message object
			args: Message content split by whitespace
		"""
		file = open(".botcontrollers", "r")
		controllers = file.readlines()
		file.close()
		controllers = filter(lambda x: x.strip() != args[2], controllers)
		file = open(".botcontrollers", "w")
		for controller in controllers:
			file.write(controller)
		file.close()
		await self.reply(message, "Removed user ID {0} from bot controllers".format(args[2]))

	def isValidBotName(self, botname):
		"""Determine whether a given name is a valid bot name

		Args:
			botname: Name to check

		Return:
			Whether the name is a valid bot name
		"""
		return not re.search("[^a-zA-Z]", botname)

	def getHandler(self, message, args):
		if not self.isBotController(message.author):
			return None
		return super().getHandler(message, args)

	def update(self):
		"""Updates the local git repository

		Return:
			Written feedback on the operation's outcome
		"""
		ret = subprocess.check_output("git fetch -q origin; git log HEAD..origin/master --oneline", shell=True).decode("utf-8")

		if ret == "":
			return "Was already up to date"
		else:
			subprocess.check_output("git pull -q".split())
			return "Updated repository"

	def startBot(self, botname):
		"""Launches a bot

		Args:
			botname: Name of bot to launch

		Return:
			Written feedback on the operation's outcome
		"""
		self.pollProcs()
		record = self.dbc.execute("SELECT * FROM procs WHERE botname=?", (botname,)).fetchone()
		if record is not None:
			return "{0} already running.".format(botname)
		p = subprocess.Popen(["python3", "bots/{0}.py".format(botname)])
		self.dbc.execute("INSERT INTO procs VALUES (?, ?)", (botname, p.pid))
		return "Started {0} pid {1}".format(botname, p.pid)

	def terminateBot(self, bot):
		"""Terminates a bot using SIGTERM

		Args:
			bot: Name of bot to terminate

		Return:
			Written feedback on the operation's outcome
		"""
		record = self.dbc.execute("SELECT * FROM procs WHERE botname=?", (bot,)).fetchone()
		if record is not None:
			pid = tuple(record)[1]
			subprocess.Popen(["kill", "-TERM", str(pid)])
			self.pollProcs()
			return "Killed {0}".format(bot)
		return "Bot {0} not found".format(bot)

	def pollProcs(self):
		"""Checks which bots are still running and deletes any dead bots from the database
		"""
		i = 0
		for botname, pid in [tuple(record) for record in self.dbc.execute("SELECT * FROM procs")]:
			p = subprocess.Popen(["ps", str(pid)])
			p.wait()
			if p.returncode != 0:
				self.dbc.execute("DELETE FROM procs WHERE botname=? AND pid=?", (botname, pid))
			else:
				i += 1
		self.db.commit()

if __name__ == "__main__":
	bot = Titan()
	bot.run(bot.getToken())
