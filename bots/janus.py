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

import discord
import asyncio
from random import randint

client = discord.Client()

name = "janus"

polls = {}
openPolls = 0

@client.event
@asyncio.coroutine
def on_ready():
	print("Logged in as " + client.user.name)

@asyncio.coroutine
def replyToMsg(msgObj, msg):
	global client
	yield from client.send_message(msgObj.channel, "{0} {1}".format(msgObj.author.mention, msg))

@client.event
@asyncio.coroutine
def on_message(message):
	global polls
	global openPolls
	if message.content.startswith(name + " "):
		if message.content.endswith(" die"):
			if openPolls > 0 and "force" not in message.content:
				yield from replyToMsg(message, "There are still polls open. Use janus force die to quit")
			yield from client.logout()
		elif message.content.endswith(" help"):
			yield from replyToMsg(message, "Janus commands:\njanus poll PollName option1 option2 ...\njanus close PollName\njanus vote PollName choice\njanus list\njanus choose option1 option2 ...");
		if client.is_closed:
			return
		args = message.content[len(name) + 1:].split(" ")
		try:
			pollname = ""
			if len(args) > 1:
				pollname = args[1]
			if args[0] == "poll":
				openPolls += 1
				polls[pollname] = {
					"owner": message.author,
					"choices": args[2:],
					"votes": {}
				}
				yield from replyToMsg(message, "Starting poll " + pollname)
			elif args[0] == "close":
				if pollname not in polls:
					yield from replyToMsg(message, "No such poll")
				if message.author != polls[pollname]["owner"]:
					yield from replyToMsg(message, "You cannot close someone else's poll")
				results = "Closing poll " + pollname + "\n"
				openPolls -= 1
				totalVotes = 0
				voteCount = {}
				for voter in polls[pollname]["votes"]:
					totalVotes += 1
					chosen = polls[pollname]["votes"][voter]
					if chosen in voteCount:
						voteCount[chosen] += 1
					else:
						voteCount[chosen] = 1
				for choice in polls[pollname]["choices"]:
					if choice not in voteCount:
						voteCount[choice] = 0
					count = voteCount[choice]
					results += "{0}: {1} ({2}%)\n".format(choice, count, count * 100 // totalVotes)
				del polls[pollname]
				yield from replyToMsg(message, results)
			elif args[0] == "vote":
				if pollname not in polls:
					yield from replyToMsg(message, "No such poll")
				if args[2] in polls[pollname]["choices"]:
					polls[pollname]["votes"][message.author] = args[2]
					yield from replyToMsg(message, "Thank you for casting your vote")
				else:
					yield from replyToMsg(message, "Available options are: {0}".format(str(polls[pollname]["choices"])))
			elif args[0] == "choose":
				options = args[1:]
				yield from replyToMsg(message, options[randint(0, len(options) - 1)])
			elif args[0] == "list":
				list = "Polls in progress:\n"
				for poll in polls:
					list += "{0} ({2})\n".format(poll, polls["choices"])
				yield from replyToMsg(message, list)
		except Exception as e:
			print(e)
			yield from replyToMsg(message, "Failed to parse your request")

file = open("tokens/" + name + ".token", "r")
token = file.read()
file.close()
client.run(token)
