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
		super().__init__("Styx", color=0x296B31)
		self.allowBotControl = True
		self.opponent = {}
		self.delta = {}
		self.guess = {}
		self.bounds = {}
		self.defaultCmd = self.handleGuess
		self.buildHelp){
			"play username lowerBound upperBound [verbose]" : "starts a new game against the specified user with the given bounds; if verbose is set, Styx will send a separate message to start the game (to be used if Styx is to play against Nix)",
			"low | correct | high" : "provide feedback for Styx' guess (the word needs to be contained in the message)"
		})
		self.about = "Hi, I'm Styx! I'm one of the smaller moons of Pluto. I'm so small that I'm more of an oblong potato than a sphere! I'm named after the river in the Greek underworld that made Achilles invulnerable - except for his heel of course."
		self.commands.update({
			"play" : self.startGame
		})

	async def handleGuess(self, message, args):
		user = message.author
		if user in self.guess:
			lowercase = [arg.lower() for arg in args]
			if "low" in lowercase:
				await self.computeGuess(message, False)
			elif "high" in lowercase:
				await self.computeGuess(message, True)
			elif "correct" in lowercase:
				del self.delta[user]
				del self.guess[user]
				await self.reply(message, "Yay!", reply=True)

	async def startGame(self, message, args):
		if len(args) < 5:
			await self.reply(message, "Usage: styx play username lowBound upBound [verbose]", reply=True)
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
				await self.reply(message, "{0} newgame {1} {2}".format(self.opponent[user], low, high))
			self.guess[user] = (high - low) / 2 + low
			self.delta[user] = self.guess[user] // 2
			self.bounds[user] = [low, high]
			await self.sendGuess(message, user)
		except ValueError:
			await self.reply(message, "Failed to parse values", reply=True)

	async def computeGuess(self, message, wasHigh):
		user = message.author
		if self.guess[user] >= self.bounds[user][1] or self.guess[user] <= self.bounds[user][0]:
			self.reply(message, self.opponent[user] + ", you've been giving me contradictory information")
			return
		if wasHigh:
			self.bounds[user][1] = self.guess[user]
			self.guess[user] -= self.delta[user]
		else:
			self.bounds[user][0] = self.guess[user]
			self.guess[user] += self.delta[user]
		if self.delta[user] > 1:
			self.delta[user] //= 2
		await self.sendGuess(message, user)

	async def sendGuess(self, message, user):
		await self.reply(message, "{0} {1}".format(self.opponent[user], int(self.guess[user])))

if __name__ == "__main__":
	bot = Styx()
	bot.run(bot.getToken())
