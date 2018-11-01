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
import subprocess
from pathlib import Path

class Deimos(CelestialBot):
	def __init__(self):
		super().__init__("Deimos")
		self.runningScripts = 0
		self.defaultCmd = self.handle

	@asyncio.coroutine
	def handle(self, message, args):
		if args[1] == "help":
			yield from self.send_message(message.channel, "To run a script, the message must start with \"deimos\" and contain two code blocks with no language. The first code block contains the script and the second is passed to `stdin`.")
		else:
			try:
				data = {}
				blocks = message.content.split("```")
				data["script"] = blocks[1].strip()
				data["input"] = blocks[3].strip() + "\n"
				resp = self.evaluate(data)
				yield from self.send_message(message.channel, "```{0}```".format(resp.decode("utf-8")))
			except:
				yield from self.send_message(message.channel, "Malformed request")

	def evaluate(self, data):
		self.runningScripts += 1
		sNum = self.runningScripts
		sFile = "script{0}".format(sNum)
		iFile = "input{0}".format(sNum)

		fds = open(sFile, "w")
		fds.write(data["script"])
		fds.close()

		fdi = open(iFile, "w")
		fdi.write(data["input"])
		fdi.close()

		ret = ""
		try:
			fdi = open(iFile, "r")
			ret = subprocess.check_output(["./vongsprache", sFile], stdin=fdi)
		except subprocess.CalledProcessError as e:
			ret = "Err {0}: {1}".format(e.returncode, e.output)
		finally:
			fdi.close()

		Path(sFile).unlink()
		Path(iFile).unlink()
		return ret

if __name__ == "__main__":
	bot = Deimos()
	bot.run(bot.getToken())
