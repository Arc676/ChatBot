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

class Styx(CelestialBot):
	def __init__(self):
		super().__init__("Styx")
		self.allowBotControl = True
		self.opponent = {}
		self.delta = {}
		self.guess = {}
		self.bounds = {}
		self.defaultCmd = self.handleGuess
		self.commands.update({
			"about" : self.getAbout,
			"play" : self.startGame
		})

	@asyncio.coroutine
	def getAbout(self, message, args):
		yield from self.replyToMsg(message, "Hi, I'm Styx! I'm one of the smaller moons of Pluto. I'm so small that I'm more of an oblong potato than a sphere! I'm named after the river in the Greek underworld that made Achilles invulnerable - except for his heel of course.")

	@asyncio.coroutine
	def handleGuess(self, message, args):
		user = message.author
		if user in self.guess:
			lowercase = [arg.lower() for arg in args]
			if "low" in lowercase:
				yield from self.computeGuess(message.channel, user, False)
			elif "high" in lowercase:
				yield from self.computeGuess(message.channel, user, True)
			elif "correct" in lowercase:
				del self.delta[user]
				del self.guess[user]
				yield from self.replyToMsg(message, "Yay!")

	@asyncio.coroutine
	def startGame(self, message, args):
		if len(args) < 5:
			yield from self.replyToMsg(message, "Usage: styx play username lowBound upBound [verbose]")
			return
		user = message.author
		if user.name != args[2]:
			for member in message.server.members:
				if member.name.upper() == args[2].upper():
					user = member
					break
		try:
			low = int(args[3])
			high = int(args[4])
			self.opponent[user] = args[2]
			if len(args) > 5 and args[5] == "verbose":
				yield from self.send_message(message.channel, "{0} newgame {1} {2}".format(self.opponent[user], low, high))
			self.guess[user] = (high - low) / 2 + low
			self.delta[user] = self.guess[user] // 2
			self.bounds[user] = [low, high]
			yield from self.sendGuess(message.channel, user)
		except ValueError:
			yield from self.replyToMsg(message, "Failed to parse values")

	@asyncio.coroutine
	def computeGuess(self, channel, user, wasHigh):
		if self.guess[user] >= self.bounds[user][1] or self.guess[user] <= self.bounds[user][0]:
			channel.send(self.opponent[user] + ", you've been giving me contradictory information")
			return
		if wasHigh:
			self.bounds[user][1] = self.guess[user]
			self.guess[user] -= self.delta[user]
		else:
			self.bounds[user][0] = self.guess[user]
			self.guess[user] += self.delta[user]
		if self.delta[user] > 1:
			self.delta[user] //= 2
		yield from self.sendGuess(channel, user)

	@asyncio.coroutine
	def sendGuess(self, channel, user):
		yield from self.send_message(channel, "{0} {1}".format(self.opponent[user], int(self.guess[user])))

if __name__ == "__main__":
	bot = Styx()
	bot.run(bot.getToken())
