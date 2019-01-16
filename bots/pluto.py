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
import asyncio
import re
from random import randint

class Pluto(CelestialBot):
	def __init__(self):
		super().__init__("Pluto", color=0xFF6200)
		self.help.description = "Type my name to get a random CAH question."
		self.about = "Pluto is a dwarf planet in our Solar System. It used to be a planet, but got demoted in 2006 after the International Astronomical Union formally defined the word 'planet' due to the increasingly large number of similarly sized objects being discovered in the Kuiper Belt and being classified as planets. In classical mythology, Pluto is the God of the Underworld."
		file = open("CAH/questions.txt", "r", encoding="utf-8")
		self.allQuestions = file.readlines()
		file.close()
		self.qCount = len(self.allQuestions) - 1
		self.defaultCmd = self.getQ

	async def getQ(self, message, args):
		"""Replies with a random CAH question

		Args:
			message: Message object
			args: Message content split by whitespace
		"""
		await self.reply(message, self.getRandomQuestion(), reply=True)

	def getRandomQuestion(self):
		"""Gets a random CAH question

		Return:
			Random question from the CAH file
		"""
		return re.sub("([\*_])", r"\\\1", self.allQuestions[randint(0, self.qCount)])

if __name__ == "__main__":
	bot = Pluto()
	bot.run(bot.getToken())
