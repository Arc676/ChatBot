# MIT License

# Copyright (c) 2017-8 Matthew Chen, Arc676/Alessandro Vinciguerra

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
import re

class Io(CelestialBot):
	callAndResponse = [
		("I love you", "I know"),
		("ping", "pong"),
		("This is madness!", "Madness?  **THIS IS SPARTA!**"),
		("There isn't enough (.+)", "Where we're going, we don't need $(s)."),
		("May the force be with you", "And also with you"),
		("Is this Tony Stank\\?", "Yes, this is the Tony Stank"),
		("where [ia][sr]e? .+\\?", "Somewhere, over the rainbow"),
		("what is .+", "42"),
		("Why did the chicken cross the road\?", "To get to the other side"),
		("LICENSE", "MIT License at https:# github.com/Arc676/Discord-Bots"),
		("Watcha doin\\?", "Eatin' chocolate"),
		("Whered'ya get it\\?", "A dog dropped it!"),
		("This isn't your average, everyday (.+)", "This is **ADVANCED** $"),
		("How many (.w+)", "ALL THE $"),
		("thank.+\\Wio\\W|thank.+\\Wio$", "You are very welcome")
	]

	def __init__(self):
		super().__init__("Io", color=0xFF9300)
		self.active = True
		self.defaultCmd = self.handle
		self.handleEverything = True
		self.buildHelp({
			"go away" : "Deactivates Io until called back",
			"come back" : "Reactivates Io",
			"rtfm" : "Provides a link to the repository for the Discord API module",
			"(assorted)" : "Io also responds to various movie quotes and assorted phrases."
		})
		self.about = "Hi, My name is Io, one of the Galilean moons of Jupiter!  I was discovered by Galileo in a telescope he built, and am the 3rd most massive of Jupiter's 69 moons.  One of my most notable feature is Tvashtar, a giant volcano."

	async def handle(self, message, args):
		"""Default message handler

		Args:
			message: Message object
			args: Message content split by whitespace
		"""
		if not self.active:
			if message.content.lower() == "io come back":
				self.active = True
				await self.reply(message, "I'm back", reply=True)
			return
		if message.content.lower() == self.name.lower():
			await self.reply(message, "Hi there!", reply=True)
		elif self.wasAddressed(message):
			if message.content.endswith(" go away"): # Makes chatbot leave
				self.active = False
				await self.reply(message, "OK :(", reply=True)
			elif message.content.endswith(" rtfm"):
				await self.reply(message, "Follow your own advice: https://github.com/Rapptz/discord.py", reply=True)
			else:
				await self.reply(message, "Yes?", reply=True)
		else: # Runs commands and performs call and response
			response = self.getReply(message.content)
			if response is not None:
				await self.reply(message, response, reply=True)

	def getReply(self, msg):
		"""Gets the appropriate reply for a message

		Args:
			msg: Message text

		Return:
			A response to the message, if any
		"""
		# Loop through array and get the appropriate response to the call
		for call, response in self.callAndResponse:
			match = re.search(call, msg, re.I)
			if match is not None:
				if '(' in call:
					response = response.replace("$", match.group(1))
				return response
		return None

if __name__ == "__main__":
	bot = Io()
	bot.run(bot.getToken())
