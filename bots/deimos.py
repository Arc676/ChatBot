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

import discord
import asyncio
import subprocess
from pathlib import Path

client = discord.Client()

name = "deimos"
runningScripts = 0

@client.event
@asyncio.coroutine
def on_ready():
	print("Logged in as " + client.user.name)

def evaluate(data):
	global runningScripts
	runningScripts += 1
	sNum = runningScripts
	sFile = "script{0}".format(sNum)
	iFile = "input{0}".format(sNum)
	runningScripts -= 1

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

@client.event
@asyncio.coroutine
def on_message(message):
	if message.author.bot:
		return
	if message.content.startswith(name):
		if message.content.endswith(" die"):
			yield from client.logout()
		elif message.content.endswith(" help"):
			yield from client.send_message(message.channel, "To run a script, the message must start with \"deimos\" and contain two code blocks with no language. The first code block contains the script and the second is passed to `stdin`.")
		else:
			try:
				data = {}
				blocks = message.content.split("```")
				data["script"] = blocks[1].strip()
				data["input"] = blocks[3].strip() + "\n"
				resp = evaluate(data)
				yield from client.send_message(message.channel, "```{0}```".format(resp.decode("utf-8")))
			except Exception as e:
				print(e)
				yield from client.send_message(message.channel, "Malformed request")

file = open("tokens/" + name + ".token", "r")
token = file.read()
file.close()
client.run(token)
