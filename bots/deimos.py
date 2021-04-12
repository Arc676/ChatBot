# MIT License

# Copyright (c) 2018-21 Arc676/Alessandro Vinciguerra

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
		super().__init__("Deimos", color=0xFFFF00)
		self.runningScripts = 0
		self.defaultCmd = self.handle
		self.help.description = "To run a script, the message must start with \"deimos\" and contain two code blocks; the first block should have `vongsprache` or `apl` as the language. The latter should have no language. The first code block should contain the script and the second the contents to be passed to `stdin`. If the latter block is omitted, no input will be passed to the script."
		self.about = "I'm Deimos, named after the smaller and outermost of Mars' two moons. I execute Vongsprache and APL scripts."

	async def handle(self, message, args):
		"""Default message handler to evaluate scripts

		Args:
			message: Message object
			args: Message content split by whitespace
		"""
		if self.wasAddressed(message):
			try:
				data = {}
				blocks = message.content.split("```")
				language, data["script"] = blocks[1].encode("utf-8").strip().decode("utf-8").split("\n", 1)
				if len(blocks) > 3:
					data["input"] = blocks[3].strip() + "\n"
				else:
					data["input"] = ""
				resp = self.evaluate(data, language)
				await self.reply(message, "```{0}```".format(resp))
			except Exception as e:
				await self.reply(message, "Malformed request. Exception:\n{0}".format(str(e)))

	def evaluate(self, data, language):
		"""Evaluates a Vongsprache script or APL code

		Args:
			data: Dictionary containing the script and desired standard input

		Return:
			Script evaluation output
		"""
		if language.lower() not in ["vongsprache", "apl"]:
			raise Exception(f"Unknown language {language}. Expected vongsprache or apl.")
		self.runningScripts += 1
		sNum = self.runningScripts
		sFile = "script{0}".format(sNum)
		iFile = "input{0}".format(sNum)

		fds = open(sFile, "wb")
		fds.write(data["script"].encode("utf-8"))
		fds.close()

		fdi = open(iFile, "w")
		fdi.write(data["input"])
		fdi.close()

		ret = ""
		try:
			fdi = open(iFile, "r")
			cmd = ["./vongsprache"] if language == "vongsprache" else ["apl", "--script", "--OFF", "-f"]
			cmd.append(sFile)
			ret = subprocess.check_output(cmd, stderr=subprocess.PIPE, stdin=fdi).decode("utf-8")
		except subprocess.CalledProcessError as e:
			ret = "Err {0}: {1}".format(e.returncode, e.stderr.decode("utf-8"))
		finally:
			fdi.close()

		Path(sFile).unlink()
		Path(iFile).unlink()
		return ret

if __name__ == "__main__":
	bot = Deimos()
	bot.run(bot.getToken())
