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

class Titan(CelestialBot):
	def __init__(self):
		super().__init__("Titan")
		self.procs = {}
		self.defaultCmd = self.handle

	@asyncio.coroutine
	def handle(self, message, args):
		if not self.isBotController(message.author):
			return
		if args[1] == "help":
			yield from self.send_message(message.channel, "Available commands: update, start bot_name [bot_name ...], kill bot_name [bot_name ...], poll, die")
		elif args[1] == "update":
			yield from self.send_message(message.channel, self.update())
		elif args[1] == "start":
			for bot in args[2:]:
				if re.search("[^a-zA-Z]", bot):
					yield from self.send_message(message.channel, "Illegal bot name")
				else:
					yield from self.send_message(message.channel, self.startBot(bot))
		elif args[1] == "kill":
			for bot in args[2:]:
				if bot in self.procs:
					subprocess.Popen(["kill", "-TERM", str(self.procs[bot])])
					yield from self.send_message(message.channel, "Killed {0}".format(bot))
			self.pollProcs()
		elif args[1] == "poll":
			self.pollProcs()
			yield from self.send_message(message.channel, "Done")

	def update(self):
		ret = subprocess.check_output("git pull -q".split(" ")).decode("utf-8")

		if ret == "":
			return "Was already up to date"
		else:
			return "Updated repository"

	def startBot(self, botname):
		self.pollProcs()
		if botname in self.procs:
			return "{0} already running.".format(botname)
		p = subprocess.Popen(["python3", "bots/{0}.py".format(botname)])
		self.procs[botname] = p.pid
		return "Started {0} pid {1}".format(botname, p.pid)

	def pollProcs(self):
		i = 0
		bots = list(self.procs.keys())
		for bot in bots:
			p = subprocess.Popen(["ps", str(self.procs[bot])])
			p.wait()
			if p.returncode != 0:
				del self.procs[bot]
			else:
				i += 1

if __name__ == "__main__":
	bot = Titan()
	bot.run(bot.getToken())
