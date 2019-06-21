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
import ctypes
import asyncio
import subprocess
import re

class Hyperion(CelestialBot):
	def __init__(self):
		super().__init__("Hyperion", color=0xD58F42)
		self.buildHelp({
			"morse [message]" : "Converts a message from normal text to Morse code",
			"text [message]" : "Converts a message from Morse code to normal text"
		})
		self.commands.update({
			"morse" : self.textToMorse,
			"text" : self.morseToText
		})
		self.about = "I'm named after Hyperion, one of Saturn's moons (also known as Saturn VII) and also the Titan god of watchfulness and observation. I can encode and decode Morse code messages!"

		# Morse library
		self.morseLib = ctypes.cdll.LoadLibrary("./libmorse.so")
		self.morseLib.textToMorse.argtypes = (ctypes.c_char_p, ctypes.c_int)
		self.morseLib.textToMorse.restype = ctypes.c_char_p
		self.morseLib.morseToText.argtypes = (ctypes.c_char_p, ctypes.c_int)
		self.morseLib.morseToText.restype = ctypes.c_char_p

		# Standard library for deallocating memory
		self.libc = ctypes.CDLL("libc.dylib")
		self.libc.free.argtypes = (ctypes.c_char_p,)

	def toMorse(self, msg):
		if re.search("[^a-zA-Z ]", msg):
			return "Invalid characters in input"
		msglen = len(msg)
		cinput = ctypes.c_char_p(msg.encode())
		coutput = self.morseLib.textToMorse(cinput, msglen)
		output = coutput.decode()
		#self.libc.free(cinput)
		#self.libc.free(coutput)
		return output

	def toText(self, msg):
		if re.search("[^.\- ]", msg):
			return "Invalid characters in input"
		msglen = len(msg)
		cinput = ctypes.c_char_p(msg.encode())
		coutput = self.morseLib.morseToText(cinput, msglen)
		output = coutput.decode()
		#self.libc.free(cinput)
		#self.libc.free(coutput)
		return output

	async def textToMorse(self, message, args):
		msg = " ".join(args[2:])
		await self.reply(message, self.toMorse(msg), reply=True)

	async def morseToText(self, message, args):
		msg = " ".join(args[2:])
		await self.reply(message, self.toText(msg), reply=True)

if __name__ == "__main__":
	bot = Hyperion()
	bot.run(bot.getToken())
