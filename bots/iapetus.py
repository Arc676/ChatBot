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
		self.handleEverything = True
		self.defaultCmd = self.checkReminder
		self.help = """Commands available for Iapetus:
countdown Event Name YYYY-MM-DD -- adds a new countdown with the given name and date to your list
delete Event Name -- deletes all events with the given name from your countdowns
list -- lists all your countdowns
help -- shows this help message
about -- shows information about Iapetus"""
		self.about = "Iapetus is believed to be the Greek God of mortality. I share this name with one of Saturn's moons because my function is to provide a countdown to the inevitable."
		self.commands.update({
			"countdown" : self.addCountdown,
			"list" : self.listCountdowns,
			"delete" : self.removeCountdown
		})
		self.db = sqlite3.connect("iapetus.db")
		self.dbc = self.db.cursor()
		try:
			self.dbc.execute("CREATE TABLE dates (name text, date text, owner text)")
			self.dbc.execute("CREATE TABLE lastReminder (owner text, date text)")
		except sqlite3.OperationalError:
			pass

	async def checkReminder(self, message, args):
		lastReminder = self.dbc.execute("SELECT date FROM lastReminder WHERE owner=?", (message.author.id,)).fetchone()
		if lastReminder is not None:
			lastReminder = tuple(lastReminder)[0]
			lastRemDate = datetime.datetime.strptime(str(lastReminder), "%Y-%m-%d").date()
			if self.daysUntil(lastRemDate) < 0:
				self.updateUserReminderDate(message.author)
				if len(list(self.getUserCountdowns(message.author))) > 0:
					await self.listCountdowns(message, args)

	async def addCountdown(self, message, args):
		if len(args) < 4:
			return
		try:
			name = " ".join(args[2:-1])
			date = args[-1]
			ddate = datetime.datetime.strptime(date, "%Y-%m-%d").date()
			remaining = self.daysUntil(ddate)
			if remaining == 0:
				await self.replyToMsg(message, "That's today!")
			elif remaining < 0:
				await self.replyToMsg(message, "{0} was {1} days ago.".format(name, -remaining))
			else:
				self.dbc.execute("INSERT INTO dates VALUES (?, ?, ?)", (name, date, message.author.id))

				# check if user has an entry in lastReminder
				if self.dbc.execute("SELECT * FROM lastReminder WHERE owner=?", (message.author.id,)).fetchone() is None:
					today = datetime.date.today().isoformat()
					self.dbc.execute("INSERT INTO lastReminder VALUES (?, ?)", (message.author.id, today))

				await self.replyToMsg(message, "Added countdown for {0}. Only {1} day(s) to go!".format(name, self.daysUntil(ddate)))
		except Exception as e:
			print(e)
			await self.replyToMsg(message, "Something went wrong parsing your request")
		self.db.commit()

	async def removeCountdown(self, message, args):
		if len(args) < 3:
			return
		event = " ".join(args[2:])
		data = (event, message.author.id)
		before = int(self.dbc.execute("SELECT COUNT(*) FROM dates WHERE name=? AND owner=?", data).fetchone()[0])
		self.dbc.execute("DELETE FROM dates WHERE name=? AND owner=?", data)
		now = int(self.dbc.execute("SELECT COUNT(*) FROM dates WHERE name=? AND owner=?", data).fetchone()[0])
		if now < before:
			await self.replyToMsg(message, "Deleted {0} countdown(s) named {1}".format(before - now, event))
		else:
			await self.replyToMsg(message, "Couldn't find an event with the given name")
		self.db.commit()

	async def listCountdowns(self, message, args):
		self.updateUserReminderDate(message.author)
		events = self.getUserCountdowns(message.author)
		count = 0
		pastEvents = []

		resp = "Your countdowns:"
		today = ""
		past = ""
		for event in events:
			count += 1
			data = tuple(event)

			name = data[0]
			date = datetime.datetime.strptime(data[1], "%Y-%m-%d").date()
			remaining = self.daysUntil(date)

			if remaining == 0:
				today += "\n{0} is today!".format(name)
				pastEvents.append(data)
			elif remaining < 0:
				past += "\n{0} was {1} days ago".format(name, -remaining)
				pastEvents.append(data)
			else:
				resp += "\nDays until {0}: {1}".format(name, remaining)

		if today != "":
			resp += "\n{0}".format(today)
		if past != "":
			resp += "\n{0}".format(past)

		if count == 0:
			resp = "You have no countdowns"

		await self.replyToMsg(message, resp)

		toDelete = len(pastEvents)
		if toDelete > 0:
			for eventData in pastEvents:
				self.dbc.execute("DELETE FROM dates WHERE name=? AND date=? AND owner=?", eventData)
			await self.replyToMsg(message, "Deleted {0} events that are either today or in the past".format(toDelete))

	def updateUserReminderDate(self, user):
		now = datetime.date.today().isoformat()
		self.dbc.execute("UPDATE lastReminder SET date=? WHERE owner=?", (now, user.id))
		self.db.commit()

	def getUserCountdowns(self, user):
		return self.dbc.execute("SELECT * FROM dates WHERE owner=?", (user.id,))

	def daysUntil(self, date):
		return (date - datetime.date.today()).days

if __name__ == "__main__":
	bot = Iapetus()
	bot.run(bot.getToken())
