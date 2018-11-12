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
from random import randint

class Nix(CelestialBot):
	def __init__(self):
		super().__init__("Nix", color=0xB86B81)
		self.answers = {}
		self.allowBotControl = True
		self.defaultCmd = self.handle
		self.buildHelp({
			"newgame lowerBound upperBound" : "Starts a new number guess game with the answer lying between the given bounds",
			"[a number]" : "Guess the number and Nix will provide feedback"
		})
		self.about = "Hi! My name is Nix, one of the moons of Pluto! Unlike Charon, I was discovered recently along with Kerberos, Hydra, and my fellow bot Styx. I'm named after the Greek embodiment of night and darkness, but the spelling was changed so I would not be confused for an asteroid named Nyx."

	async def handle(self, message, args):
		if "newgame" in args:
			if len(args) != 4:
				await self.reply(message, "Usage: nix newgame lowBound upBound", reply=True)
				return
			try:
				lowerBound = int(args[2])
				upperBound = int(args[3])
				self.answers[message.author] = randint(lowerBound, upperBound)
				await self.reply(message, "Alright, let's play!", reply=True)
			except ValueError:
				await self.reply(message, "Failed to parse arguments", reply=True)
		elif message.author in self.answers:
			try:
				guess = int(args[1])
				if guess == self.answers[message.author]:
					del self.answers[message.author]
					await self.reply(message, "Correct", reply=True)
				elif guess < self.answers[message.author]:
					await self.reply(message, "Too low", reply=True)
				else:
					await self.reply(message, "Too high", reply=True)
			except ValueError:
				await self.reply(message, "Failed to parse guess", reply=True)

if __name__ == "__main__":
	bot = Nix()
	bot.run(bot.getToken())
