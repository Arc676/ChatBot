//MIT License

//Copyright (c) 2017 Arc676/Alessandro Vinciguerra

//Permission is hereby granted, free of charge, to any person obtaining a copy
//of this software and associated documentation files (the "Software"), to deal
//in the Software without restriction, including without limitation the rights
//to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//copies of the Software, and to permit persons to whom the Software is
//furnished to do so, subject to the following conditions:

//The above copyright notice and this permission notice shall be included in all
//copies or substantial portions of the Software.

//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//SOFTWARE.

const fs = require('fs')
const Discord = require('discord.js')
const client = new Discord.Client()

var name = "janus"

var polls = {}
var openPolls = 0

client.on('ready', () => {
	console.log(`Logged in as ${client.user.username}`)
})

client.on('message', message => {
	if (message.content.startsWith(name + ' ')) {
		if (message.content.endsWith(' die')) {
			if (openPolls > 0 && message.content.indexOf("force") === -1) {
				message.reply("There are still polls open. Use janus force die to quit")
				return
			}
			client.destroy()
			process.exit(0)
		}
		const args = message.content.substring(name.length + 1).split(" ")
		try {
			const pollname = args[1];
			if (args[0] === "poll") {
				message.reply("Starting poll " + pollname);
				openPolls++
				polls[pollname] = {
					owner: message.author,
					choices: args.slice(2),
					votes: {}
				}
			} else if (args[0] === "close") {
				if (!(pollname in polls)) {
					message.reply("No such poll")
				}
				if (message.author !== polls[pollname].owner) {
					message.reply("You cannot close someone else's poll")
					return
				}
				var results = "Closing poll " + pollname + "\n"
				openPolls--
				var totalVotes = 0
				var voteCount = {}
				for (var voter in polls[pollname].votes) {
					totalVotes++
					const chosen = polls[pollname].votes[voter]
					if (chosen in voteCount) {
						voteCount[chosen]++
					} else {
						voteCount[chosen] = 1
					}
				}
				for (var i = 0; i < polls[pollname].choices.length; i++) {
					const choice = polls[pollname].choices[i]
					if (!(choice in voteCount)) {
						voteCount[choice] = 0
					}
					const count = voteCount[choice]
					results += choice + ": " + count + " (" + (count * 100/ totalVotes) + "%)\n"
				}
				delete polls[pollname]
				message.reply(results)
			} else if (args[0] === "vote") {
				if (!(pollname in polls)) {
					message.reply("No such poll")
					return
				}
				if (polls[pollname].choices.includes(args[2])) {
					polls[pollname].votes[message.author] = args[2]
					message.reply("Thank you for casting your vote")
				} else {
					message.reply("Available options are: " + polls[pollname].choices)
				}
			} else if (args[0] === "choose") {
				const options = args.slice(1)
				message.reply(options[Math.floor(Math.random() * options.length)])
			} else if (args[0] === "list") {
				list = "Polls in progress:\n"
				for (var poll in polls) {
					list += poll + " (" + polls[poll].choices + ")\n"
				}
				message.reply(list)
			}
		} catch (e) {
			message.reply("Failed to parse your request")
		}

	}
})

client.login(fs.readFileSync('tokens/' + name + '.token', 'utf8'))
