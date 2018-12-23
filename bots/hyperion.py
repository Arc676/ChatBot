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
import asyncio
import discord
import subprocess
import re

class Hyperion(CelestialBot):
	def __init__(self):
		super().__init__("Hyperion", color=0xD58F42)
		self.commands.update({
			"morse" : self.textToMorse,
			"text" : self.morseToText
		})

	def convert(self, msg, toMorse):
		ret = ""
		flag = "-t"
		if not toMorse:
			if re.search("[^.\- ]", msg):
				return "Invalid characters in input"
			flag = "-m"
		try:
			ret = subprocess.check_output(["./morse", flag,  msg], stderr=subprocess.PIPE).decode("utf-8")
		except subprocess.CalledProcessError as e:
			ret = "Err {0}: {1}".format(e.returncode, e.stderr.decode("utf-8"))
		return "```{0}```".format(ret)

	async def textToMorse(self, message, args):
		msg = " ".join(args[2:])
		await self.reply(message, self.convert(msg, True), reply=True)

	async def morseToText(self, message, args):
		msg = " ".join(args[2:])
		await self.reply(message, self.convert(msg, False), reply=True)

if __name__ == "__main__":
	bot = Hyperion()
	bot.run(bot.getToken())
