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

class Janus(CelestialBot):
	def __init__(self):
		super().__init__("Janus")
		self.polls = {}
		self.openPolls = 0
		self.help = """Commands available for Janus
poll PollName option1 option2 [option3 ..] -- creates a new poll named PollName; this name cannot have spaces; at least 2 choices must be available
close PollName -- closes the poll PollName and shows the results
vote PollName choice -- votes for 'choice' in the poll 'PollName'
list -- shows all currently running polls
choose option1 option2 [option3 ...] -- randomly chooses between the options; there must be at least two choices available"""
		self.about = "I'm Janus, named after the Roman God of beginnings and ends; duality; gates, doorways, and passageways; transitions; and time. I also share my name with an inner satellite of Saturn, also known as Saturn X."
		self.commands.update({
			"poll" : self.newPoll,
			"close" : self.closePoll,
			"vote" : self.voteOnPoll,
			"list" : self.listPolls,
			"choose" : self.chooseFromList
		})

	async def newPoll(self, message, args):
		if len(args) < 4:
			await self.replyToMsg("Invalid request")
			return
		pollname = args[2]
		self.openPolls += 1
		self.polls[pollname] = {
			"owner": message.author,
			"choices": args[3:],
			"votes": {}
		}
		await self.replyToMsg(message, "Starting poll " + pollname)

	async def closePoll(self, message, args):
		if len(args) < 3:
			await self.replyToMsg(message, "Invalid request")
			return
		pollname = args[2]
		if pollname not in self.polls:
			await replyToMsg(message, "No such poll")
			return
		if message.author != self.polls[pollname]["owner"]:
			await self.replyToMsg(message, "You cannot close someone else's poll")
			return
		results = "Closing poll " + pollname + "\n"
		self.openPolls -= 1
		totalVotes = 0
		voteCount = {}
		for _, chosen in self.polls[pollname]["votes"].items():
			totalVotes += 1
			if chosen in voteCount:
				voteCount[chosen] += 1
			else:
				voteCount[chosen] = 1
		if totalVotes == 0:
			results += "Nobody voted"
		else:
			for choice in self.polls[pollname]["choices"]:
				if choice not in voteCount:
					voteCount[choice] = 0
				count = voteCount[choice]
				results += "{0}: {1} ({2}%)\n".format(choice, count, count * 100 // totalVotes)
		del self.polls[pollname]
		await self.replyToMsg(message, results)

	async def voteOnPoll(self, message, args):
		if len(args) < 4:
			await self.replyToMsg(message, "Invalid vote")
			return
		pollname = args[2]
		if pollname not in self.polls:
			await self.replyToMsg(message, "No such poll")
		if args[3] in self.polls[pollname]["choices"]:
			self.polls[pollname]["votes"][message.author] = args[3]
			await self.replyToMsg(message, "Thank you for casting your vote")
		else:
			await self.replyToMsg(message, "Available options are: {0}".format(str(self.polls[pollname]["choices"])))

	async def chooseFromList(self, message, args):
		if len(args) < 4:
			await self.replyToMsg(message, "Need at least 2 items to choose from")
			return
		options = args[2:]
		await self.replyToMsg(message, options[randint(0, len(options) - 1)])

	async def listPolls(self, message, args):
		list = "Polls in progress:\n"
		for pollname, poll in self.polls.items():
			list += "{0} ({1})\n".format(pollname, poll["choices"])
		await self.replyToMsg(message, list)

if __name__ == "__main__":
	bot = Janus()
	bot.run(bot.getToken())
