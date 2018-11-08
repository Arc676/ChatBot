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
		super().__init__("Titan")
		self.commands.update({
			"help" : self.printHelp,
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

	@asyncio.coroutine
	def printHelp(self, message, args):
		yield from self.send_message(message.channel, "Available commands: update, start|kill|restart bot_name [bot_name ...], list, die")

	@asyncio.coroutine
	def updateRepo(self, message, args):
		yield from self.send_message(message.channel, self.update())

	@asyncio.coroutine
	def launchBot(self, message, args):
		for bot in args[2:]:
			if self.isValidBotName(bot):
				yield from self.send_message(message.channel, self.startBot(bot))
			else:
				yield from self.send_message(message.channel, "Illegal bot name")
		self.db.commit()

	@asyncio.coroutine
	def kill(self, message, args):
		for bot in args[2:]:
			yield from self.send_message(message.channel, self.terminateBot(bot))
		self.pollProcs()
		self.db.commit()

	@asyncio.coroutine
	def restart(self, message, args):
		for bot in args[2:]:
			if self.isValidBotName(bot):
				resp = self.terminateBot(bot) + "\n"
				resp += self.startBot(bot)
				yield from self.send_message(message.channel, resp)
			else:
				yield from self.send_message(message.channel, "Illegal bot name")

	@asyncio.coroutine
	def listBots(self, message, args):
		self.pollProcs()
		resp = "Running bots:\n{0}".format(
			"\n".join([(lambda x: "Name: {0}, PID: {1}".format(x[0], x[1]))(tuple(record))
				for record in self.dbc.execute("SELECT * FROM procs")])
		)
		yield from self.send_message(message.channel, resp)

	def isValidBotName(self, botname):
		return not re.search("[^a-zA-Z]", botname)

	def getHandler(self, message, args):
		if not self.isBotController(message.author):
			return None
		return super().getHandler(message, args)

	def update(self):
		ret = subprocess.check_output("git fetch -q origin; git log HEAD..origin/master --oneline", shell=True).decode("utf-8")

		if ret == "":
			return "Was already up to date"
		else:
			subprocess.check_output("git pull -q".split())
			return "Updated repository"

	def startBot(self, botname):
		self.pollProcs()
		record = self.dbc.execute("SELECT * FROM procs WHERE botname=?", (botname,)).fetchone()
		if record is not None:
			return "{0} already running.".format(botname)
		p = subprocess.Popen(["python3", "bots/{0}.py".format(botname)])
		self.dbc.execute("INSERT INTO procs VALUES (?, ?)", (botname, p.pid))
		return "Started {0} pid {1}".format(botname, p.pid)

	def terminateBot(self, bot):
		record = self.dbc.execute("SELECT * FROM procs WHERE botname=?", (bot,)).fetchone()
		if record is not None:
			pid = tuple(record)[1]
			subprocess.Popen(["kill", "-TERM", str(pid)])
			self.pollProcs()
			return "Killed {0}".format(bot)
		return "Bot {0} not found".format(bot)

	def pollProcs(self):
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
