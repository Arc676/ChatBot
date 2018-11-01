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
		super().__init__("Nix")
		self.answers = {}
		self.allowBotControl = True
		self.defaultCmd = self.handle

	@asyncio.coroutine
	def handle(self, message, args):
		if message.content.endswith(" about"): 
			yield from self.replyToMsg(message, "Hi! My name is Nix, one of the moons of Pluto! Unlike Charon, I was discovered recently along with Kerberos, Hydra, and my fellow bot Styx. I'm named after the Greek embodiment of night and darkness, but the spelling was changed so I would not be confused for an asteroid named Nyx.")
		elif "newgame" in args:
			if len(args) != 4:
				yield from self.replyToMsg(message, "Usage: nix newgame lowBound upBound")
				return
			try:
				lowerBound = int(args[2])
				upperBound = int(args[3])
				self.answers[message.author] = randint(lowerBound, upperBound)
				yield from self.replyToMsg(message, "Alright, let's play!")
			except ValueError:
				yield from self.replyToMsg(message, "Failed to parse arguments")
		elif message.author in self.answers:
			try:
				guess = int(args[1])
				if guess == self.answers[message.author]:
					del self.answers[message.author]
					yield from self.replyToMsg(message, "Correct")
				elif guess < self.answers[message.author]:
					yield from self.replyToMsg(message, "Too low")
				else:
					yield from self.replyToMsg(message, "Too high")
			except ValueError:
				yield from self.replyToMsg(message, "Failed to parse guess")

if __name__ == "__main__":
	bot = Nix()
	bot.run(bot.getToken())
