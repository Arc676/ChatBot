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

import discord
import asyncio
from random import randint

client = discord.Client()

name = "prometheus"

@client.event
@asyncio.coroutine
def on_ready():
	print("Logged in as " + client.user.name)

def pick(options):
	return options[randint(0, len(options) - 1)]

def generateFact():
	return "Did you know that {0} {1} because of {2}? Apparently {3}. While it may seem like trivia, it {4}.".format(
		pick([
			"the {0} equinox".format(
				pick(["fall", "spring"])
			),
			"the {0} {1}".format(
				pick(["summer", "winter"]),
				pick(["solstice", "olympics"])
			),
			"the {0} {1}".format(
				pick(["earliest", "latest"]),
				pick(["sunrise", "sunset"])
			),
			"daylight {0} time".format(
				pick(["savings", "saving"])
			),
			"leap {0}".format(
				pick(["day", "year"])
			),
			"Easter",
			"the {0} moon".format(
				pick(["super", "blood", "harvest"])
			),
			"Toyota truck month",
			"shark week"
		]),
		pick([
			"happens {0} every year".format(
				pick(["earlier", "later", "at the wrong time"])
			),
			"drifts out of sync with the {0}".format(
				pick([
					"sun",
					"moon",
					"zodiac",
					"{0} calendar".format(
						pick(["Gregorian", "Mayan", "lunar", "iPhone"])
					),
					"atomic clock in Colorado"
				])
			),
			"might {0} this year".format(
				pick(["not happen", "happen twice"])
			)
		]),
		pick([
			"time zone legislation in {0}".format(
				pick(["Indiana", "Arizona", "Russia"])
			),
			"a decree by the Pope in the 1500s",
			"{0} of the {1}".format(
				pick(["precession", "libration", "nutation", "libation", "eccentricity", "obliquity"]),
				pick([
					"moon",
					"sun",
					"Earth's axis",
					"equator",
					"prime meridian",
					"{0} line".format(
						pick(["international date", "Mason-Dixon"])
					)
				])
			),
			"magnetic field reversal",
			"an arbitrary decision by {0}".format(
				pick(["Benjamin Franklin", "Isaac Newton", "FDR"])
			)
		]),
		pick([
			"it causes a predicable increase in car accidents",
			"that's why we have leap seconds",
			"scientists are really worried",
			"it was even more extreme during the {0}".format(
				pick(["Bronze Age", "Ice Age", "Cretaceous", "1990s"])
			),
			"there's a proposal to fix it, but it {0}".format(
				pick([
					"will never happen",
					"actually makes things worse",
					"is stalled in congress",
					"might be unconstitutional"
				])
			),
			"it's getting worse and no one knows why"
		]),
		pick([
			"causes huge headaches for software developers",
			"is taken advantage of by high-speed traders",
			"triggered the 2003 Northeast Blackout",
			"has to be corrected for by GPS satellites",
			"is now recognized as a major cause of World War I"
		])
	)

@asyncio.coroutine
def replyToMsg(msgObj, msg):
	global client
	yield from client.send_message(msgObj.channel, "{0} {1}".format(msgObj.author.mention, msg))

@client.event
@asyncio.coroutine
def on_message(message):
	if message.content.startswith(name + " "):
		if message.content.endswith(" die"):
			yield from client.logout()
		elif message.content.endswith(" about"): 
			yield from replyToMsg(message, "Hi! My name is Prometheus. I'm one of Saturn's satellites. The picture you see was taken by Cassini. I'm named after the Greek Titan who created humans from clay and stole fire from the Gods. Prometheus also featured on xkcd 1228.")
		elif message.content.endswith(" 1228"):
			yield from replyToMsg(message, "https://xkcd.com/1228/")
		elif message.content.endswith(" 1930"):
			yield from replyToMsg(message, "https://xkcd.com/1930/")
		elif message.content.endswith(" fact"):
			fact = generateFact()
			yield from replyToMsg(message, fact)
		elif message.content.endswith(" help"):
			yield from replyToMsg(message, "Type \"prometheus\" followed by about, die, 1228, 1930, or fact")

file = open("tokens/" + name + ".token", "r")
token = file.read()
file.close()
client.run(token)
