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
import re
from random import randint

class Charon(CelestialBot):
	def __init__(self):
		super().__init__("Charon")
		self.help = "Type my name to get a random CAH answer. Optionally, add a number after my name to get that many answers at once"
		self.about = "I'm Charon, named after the largest of Pluto's moons. Charon is the ferryman of the dead in Greek mythology."
		file = open("CAH/answers.txt", "r", encoding="utf-8")
		self.allAnswers = file.readlines()
		file.close()
		self.aCount = len(self.allAnswers) - 1
		self.defaultCmd = self.getA

	async def getA(self, message, args):
		times = 1
		if len(args) > 1:
			try:
				times = int(args[1])
			except:
				pass
		answer = ""
		for i in range(times):
			answer += self.getRandomAnswer()
		await self.send_message(message.channel, "{0} {1}".format(message.author.mention, answer.rstrip()))

	def getRandomAnswer(self):
		return re.sub("([\*_])", r"\\\1", self.allAnswers[randint(0, self.aCount)])

if __name__ == "__main__":
	bot = Charon()
	bot.run(bot.getToken())
