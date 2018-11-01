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
import datetime

class Iapetus(CelestialBot):
	def __init__(self):
		super().__init__("Iapetus")
		self.dates = {}
		self.defaultCmd = self.printInfo
		self.commands.update({
			"countdown" : self.addCountdown,
			"list" : self.listCountdowns,
			"delete" : self.removeCountdown
		})

	@asyncio.coroutine
	def printInfo(self, message, args):
		if args[1] == "help":
			yield from self.send_message(message.channel, "Available commands: countdown event_name YYYY-MM-DD, delete event_name, list, die, help, about")
		elif args[1] == "about":
			yield from self.send_message(message.channel, "Iapetus is believed to be the Greek God of mortality. I share this name with one of Saturn's moons because my function is to provide a countdown to the inevitable.")

	@asyncio.coroutine
	def addCountdown(self, message, args):
		if len(args) < 4:
			return
		try:
			components = [int(c) for c in args[-1].split("-")]
			name = " ".join(args[2:-1])
			date = datetime.date(components[0], components[1], components[2])
			if message.author not in self.dates:
				self.dates[message.author] = []
			self.dates[message.author].append({
				"name" : name,
				"date" : date
			})
			yield from self.replyToMsg(message, "Added countdown for {0}. Only {1} day(s) to go!".format(name, self.daysUntil(date)))
		except:
			yield from self.replyToMsg(message, "Something went wrong parsing your request")

	@asyncio.coroutine
	def removeCountdown(self, message, args):
		if len(args) < 3:
			return
		idxs = [idx for idx in range(len(self.dates[message.author])) if self.dates[message.author][idx]["name"] == args[2]]
		if len(idxs) > 0:
			del self.dates[message.author][idxs[0]]
			yield from self.replyToMsg(message, "Deleted countdown for event {0}".format(args[2]))
			if len(idxs) > 1:
				yield from self.replyToMsg(message, "You still have {0} event(s) named {1}".format(len(idxs) - 1, args[2]))
		else:
			yield from self.replyToMsg(message, "Couldn't find an event with the given name")

	@asyncio.coroutine
	def listCountdowns(self, message, args):
		resp = "Your countdowns:"
		if message.author in self.dates and len(self.dates[message.author]) > 0:
			for event in self.dates[message.author]:
				resp += "\nDays until {0}: {1}".format(event["name"], self.daysUntil(event["date"]))
		else:
			resp = "You have no countdowns"
		yield from self.replyToMsg(message, resp)

	def daysUntil(self, date):
		return (date - datetime.date.today()).days

if __name__ == "__main__":
	bot = Iapetus()
	bot.run(bot.getToken())
