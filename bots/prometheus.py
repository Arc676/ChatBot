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
from random import randint
import asyncio

class Prometheus(CelestialBot):
	def __init__(self):
		super().__init__("Prometheus", color=0xFF8D32)
		self.defaultCmd = self.printInfo
		self.buildHelp({
			"fact" : "Generates a random calendar fact from the options available in xkcd 1930",
			"1228 | 1930" : "Provides a link to the xkcd comic with the given number, both of which are related to Prometheus' functionality"
		})
		self.about = "Hi! My name is Prometheus. I'm one of Saturn's satellites. The picture on my profile was taken by Cassini. I'm named after the Greek Titan who created humans from clay and stole fire from the Gods. Prometheus also featured on xkcd 1228."
		self.commands.update({
			"fact" : self.replyWithFact
		})

	async def printInfo(self, message, args):
		if args[1] == "1228":
			await self.reply(message, "https://xkcd.com/1228/", reply=True)
		elif args[1] == "1930":
			await self.reply(message, "https://xkcd.com/1930/", reply=True)

	@staticmethod
	def pick(options):
		return options[randint(0, len(options) - 1)]

	@staticmethod
	def generateFact():
		return "Did you know that {0} {1} because of {2}? Apparently {3}. While it may seem like trivia, it {4}.".format(
			Prometheus.pick([
				"the {0} equinox".format(
					Prometheus.pick(["fall", "spring"])
				),
				"the {0} {1}".format(
					Prometheus.pick(["summer", "winter"]),
					Prometheus.pick(["solstice", "olympics"])
				),
				"the {0} {1}".format(
					Prometheus.pick(["earliest", "latest"]),
					Prometheus.pick(["sunrise", "sunset"])
				),
				"daylight {0} time".format(
					Prometheus.pick(["savings", "saving"])
				),
				"leap {0}".format(
					Prometheus.pick(["day", "year"])
				),
				"Easter",
				"the {0} moon".format(
					Prometheus.pick(["super", "blood", "harvest"])
				),
				"Toyota truck month",
				"shark week"
			]),
			Prometheus.pick([
				"happens {0} every year".format(
					Prometheus.pick(["earlier", "later", "at the wrong time"])
				),
				"drifts out of sync with the {0}".format(
					Prometheus.pick([
						"sun",
						"moon",
						"zodiac",
						"{0} calendar".format(
							Prometheus.pick(["Gregorian", "Mayan", "lunar", "iPhone"])
						),
						"atomic clock in Colorado"
					])
				),
				"might {0} this year".format(
					Prometheus.pick(["not happen", "happen twice"])
				)
			]),
			Prometheus.pick([
				"time zone legislation in {0}".format(
					Prometheus.pick(["Indiana", "Arizona", "Russia"])
				),
				"a decree by the Pope in the 1500s",
				"{0} of the {1}".format(
					Prometheus.pick(["precession", "libration", "nutation", "libation", "eccentricity", "obliquity"]),
					Prometheus.pick([
						"moon",
						"sun",
						"Earth's axis",
						"equator",
						"prime meridian",
						"{0} line".format(
							Prometheus.pick(["international date", "Mason-Dixon"])
						)
					])
				),
				"magnetic field reversal",
				"an arbitrary decision by {0}".format(
					Prometheus.pick(["Benjamin Franklin", "Isaac Newton", "FDR"])
				)
			]),
			Prometheus.pick([
				"it causes a predicable increase in car accidents",
				"that's why we have leap seconds",
				"scientists are really worried",
				"it was even more extreme during the {0}".format(
					Prometheus.pick(["Bronze Age", "Ice Age", "Cretaceous", "1990s"])
				),
				"there's a proposal to fix it, but it {0}".format(
					Prometheus.pick([
						"will never happen",
						"actually makes things worse",
						"is stalled in congress",
						"might be unconstitutional"
					])
				),
				"it's getting worse and no one knows why"
			]),
			Prometheus.pick([
				"causes huge headaches for software developers",
				"is taken advantage of by high-speed traders",
				"triggered the 2003 Northeast Blackout",
				"has to be corrected for by GPS satellites",
				"is now recognized as a major cause of World War I"
			])
		)

	async def replyWithFact(self, message, args):
		fact = Prometheus.generateFact()
		await self.reply(message, fact, reply=True)

if __name__ == "__main__":
	bot = Prometheus()
	bot.run(bot.getToken())
