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
import sqlite3

class Iapetus(CelestialBot):
	def __init__(self):
		super().__init__("Iapetus")
		self.defaultCmd = self.printInfo
		self.commands.update({
			"countdown" : self.addCountdown,
			"list" : self.listCountdowns,
			"delete" : self.removeCountdown
		})
		self.db = sqlite3.connect("iapetus.db")
		self.dbc = self.db.cursor()
		try:
			self.dbc.execute("CREATE TABLE dates (name text, date text, owner text)")
		except sqlite3.OperationalError:
			pass

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
			name = " ".join(args[2:-1])
			date = args[-1]
			ddate = datetime.datetime.strptime(date, "%Y-%m-%d").date()
			self.dbc.execute("INSERT INTO dates VALUES (?, ?, ?)", (name, date, message.author.id))
			yield from self.replyToMsg(message, "Added countdown for {0}. Only {1} day(s) to go!".format(name, self.daysUntil(ddate)))
		except Exception as e:
			print(e)
			yield from self.replyToMsg(message, "Something went wrong parsing your request")
		self.db.commit()

	@asyncio.coroutine
	def removeCountdown(self, message, args):
		if len(args) < 3:
			return
		if self.dbc.execute("DELETE FROM dates WHERE name=?", args[2]).rowcount > 0:
			yield from self.replyToMsg(message, "Deleted countdown(s) named {0}".format(args[2]))
		else:
			yield from self.replyToMsg(message, "Couldn't find an event with the given name")
		self.db.commit()

	@asyncio.coroutine
	def listCountdowns(self, message, args):
		resp = "Your countdowns:"
		events = self.dbc.execute("SELECT * FROM dates WHERE owner=?", (message.author.id,))
		count = 0
		for event in events:
			count += 1
			data = tuple(event)
			name = data[0]
			date = datetime.datetime.strptime(data[1], "%Y-%m-%d").date()
			resp += "\nDays until {0}: {1}".format(name, self.daysUntil(date))
		if count == 0:
			resp = "You have no countdowns"
		yield from self.replyToMsg(message, resp)

	def daysUntil(self, date):
		return (date - datetime.date.today()).days

if __name__ == "__main__":
	bot = Iapetus()
	bot.run(bot.getToken())
