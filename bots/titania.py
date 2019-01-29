# MIT License

# Copyright (c) 2017-9 Arc676/Alessandro Vinciguerra

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
from discord import Embed
import asyncio
from mtgsdk import Card

class Titania(CelestialBot):
	def __init__(self):
		super().__init__("Titania", color=0x117350)
		self.resultLimit = 10
		self.handleEverything = True
		self.defaultCmd = self.search
		self.help.description = """Put queries in [[double brackets]]. Separate search parameters with spaces. Replace spaces within search parameters with plus signs.

Queries are of the form 'property=value' e.g. 'name=Arc+Lightning'. Available properties include 'name', 'cmc', 'set' (three letter abbreviation), 'type', and more. Some properties cannot be searched for due to limitations in the API e.g. 'manaCost'. An example suitable search message might be [[name=bolt cmc=1 type=instant]]"""
		self.buildHelp({
			"limit" : "Sets the limit on how many cards should be printed for any query"
		})
		self.about = "I'm Titania, named after the largest of Uranus' moons and the queen of the fairies in Shakespeare's _A Midsummer Night's Dream_. Titania is also the name of a creature in Magic the Gathering."
		self.commands.update({
			"limit" : self.setLimit
		})

	async def printCard(self, message, card):
		"""Builds an embed with a given card's data and replies to a given message with it

		Args:
			message: Message object
			card: Card object
		"""
		resp = Embed(title=card.name, color=self.color, description="{0}/{1}".format(
			card.rarity,
			", ".join(card.types)
		))
		if card.image_url is not None:
			resp.set_thumbnail(url=card.image_url)
		resp.add_field(name="Mana Cost", value=card.mana_cost, inline=False)
		if len(card.supertypes) > 0:
			resp.add_field(name="Supertypes", value=", ".join(card.supertypes), inline=False)
		if len(card.subtypes) > 0:
			resp.add_field(name="Subtypes", value=", ".join(card.subtypes), inline=False)
		resp.add_field(name="Oracle Text", value=card.text, inline=False)
		if card.power is not None:
			resp.add_field(name="P/T", value="{0}/{1}".format(
				card.power, card.toughness
			), inline=False)
		elif card.loyalty is not None:
			resp.add_field(name="Initial Loyalty", value=card.loyalty, inline=False)
		await self.reply(message, embed=resp)

	def getQueryProperties(self, query):
		"""Builds a search query from a message

		Args:
			query: Array of desired card properties

		Return:
			kwargs'able dictionary to use as a search query for cards
		"""
		properties = {}
		for param in query:
			prop = param.split("=")
			try:
				properties[prop[0]] = prop[1].replace("+", " ")
			except:
				return None
		return properties

	async def setLimit(self, message, args):
		"""Sets the maximum number of cards to be printed at once

		Args:
			message: Message object
			args: Message content split by whitespace
		"""
		if len(args) >= 3:
			self.resultLimit = int(args[2])

	async def search(self, message, args):
		"""Searches for cards matching the query in a message

		Args:
			message: Message object
			args: Message content split by whitespace
		"""
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
			debug = False
			if message.content.startswith("debug"):
				debug = True
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
				if distinct[card.name].image_url is None and card.image_url is not None:
					distinct[card.name] = card
			await self.reply(message, "Found {0} distinct card(s)".format(found), reply=True)
			if found == 0:
				return
			elif found > self.resultLimit:
				await self.reply(message, "Result count exceeds limit. Aborting.", reply=True)
				return
			for name, card in distinct.items():
				if debug:
					print("Name: {0}; card: {1}".format(name, card.__dict__))
				await self.printCard(message, card)

if __name__ == "__main__":
	bot = Titania()
	bot.run(bot.getToken())
