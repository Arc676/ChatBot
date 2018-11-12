# MIT License

# Copyright (c) 2017-8 Arc676/Alessandro Vinciguerra

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
from mtgsdk import Card

class Titania(CelestialBot):
	properties = [
		[
			"name",
			"mana_cost"
		],
		[
			"rarity",
			"types"
		],
		[
			"text"
		],
		[
			"power",
			"toughness"
		]
	]

	def __init__(self):
		super().__init__("Titania", color=0x117350)
		self.resultLimit = 10
		self.handleEverything = True
		self.defaultCmd = self.search
		self.help.description = """Put queries in [[double brackets]]. Separate search parameters with spaces. Replace spaces within search parameters with plus signs.

Queries are of the form 'property=value' e.g. 'name=Arc+Lightning'. Available properties include 'name', 'cmc', 'set' (three letter abbreviation), 'type', and more. Some properties cannot be searched for due to limitations in the API e.g. 'manaCost'. An example suitable search message might be [[name=bolt cmc=1 type=instant]]"""
		self.about = "I'm Titania, named after the largest of Uranus' moons and the queen of the fairies in Shakespeare's _A Midsummer Night's Dream_. Titania is also the name of a creature in Magic the Gathering."
		self.commands.update({
			"limit" : self.setLimit
		})

	async def printCard(self, message, card):
		text = ""
		for group in self.properties:
			j = 0
			for prop in group:
				if prop in card.__dict__:
					text += str(card.__dict__[prop])
					if j + 1 < len(group):
						text += "/"
					j += 1
			text += "\n"
		await self.reply(message, text, reply=True)

	def getQueryProperties(self, query):
		properties = {}
		for param in query:
			prop = param.split("=")
			try:
				properties[prop[0]] = prop[1].replace("+", " ")
			except:
				return None
		return properties

	async def setLimit(self, message, args):
		if len(args) >= 3:
			self.resultLimit = int(args[2])

	async def search(self, message, args):
		startIndex, endIndex = 0, 0
		try:
			startIndex = message.content.index("[[")
			endIndex = message.content.index("]]")
		except:
			startIndex = -1
		if startIndex != -1 and endIndex != -1:
			query = message.content[startIndex + 2:endIndex].split()
			if len(query) == 0:
				return
			printText = True
			printImage = False
			debug = False
			if message.content.startswith("debug"):
				debug = True
			elif message.content.startswith("image"):
				printImage = True
				printText = False
			elif message.content.startswith("combo"):
				printImage = True
			properties = self.getQueryProperties(query)
			if properties is None:
				await self.reply(message, "Sorry, your query failed", reply=True)
				return

			# search for cards
			distinct = {}
			found = 0
			for card in Card.where(**properties).all():
				if card.name not in distinct:
					distinct[card.name] = card
					found += 1
			await self.reply(message, "Found {0} distinct card(s)".format(found), reply=True)
			if found == 0:
				return
			elif found > self.resultLimit:
				await self.reply(message, "Result count exceeds limit. Aborting.", reply=True)
				return
			for name, card in distinct.items():
				if printText:
					await self.printCard(message, card)
				if printImage and "image_url" in card.__dict__:
					await self.reply(message, card.__dict__["image_url"], reply=True)
				if debug:
					print("Name: {0}; card: {1}".format(name, card.__dict__))
			await self.reply(message, "End of search results", reply=True)

if __name__ == "__main__":
	bot = Titania()
	bot.run(bot.getToken())
