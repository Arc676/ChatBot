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

var name = "styx"

var opponent = {}
var delta = {}
var guess = {}
var bounds = {}

client.on('ready', () => {
	console.log(`Logged in as ${client.user.username}`)
})

function computeGuess(channel, user, wasHigh) {
	if (guess[user] >= bounds[user][1] || guess[user] <= bounds[user][0]) {
		channel.send(opponent[user] + ", you've been giving me contradictory information")
		return
	}
	if (wasHigh) {
		bounds[user][1] = guess[user]
		guess[user] -= delta[user]
	} else {
		bounds[user][0] = guess[user]
		guess[user] += delta[user]
	}
	if (delta[user] > 1) {
		delta[user] = Math.floor(delta[user] / 2)
	}
	sendGuess(channel, user)
}

function sendGuess(channel, user) {
	channel.send(opponent[user] + ' ' + guess[user])
}

client.on('message', message => {
	if (message.mentions.users.array().includes(client.user)) {
		var user = message.author
		if (message.content.endsWith("die")) {
			client.destroy()
			process.exit(0)
		} else if (message.content.indexOf(" play ") !== -1) {
			var args = message.content.split(' ')
			if (args.length < 5) {
				message.reply("Usage: @styx play username lowBound upBound [verbose]")
				return
			}
			if (user.username !== args[2]) {
				message.guild.members.forEach(function(value, key, map){
					if (value.user.username.toUpperCase() === args[2].toUpperCase()) {
						user = value.user
						return
					}
				})
			}
			opponent[user] = args[2]
			var low = parseInt(args[3])
			var high = parseInt(args[4])
			if (args.length > 5 && args[5] === "verbose") {
				message.channel.send(opponent[user] + " newgame " + low + " " + high)
			}
			guess[user] = (high - low) / 2 + low
			delta[user] = Math.floor(guess[user] / 2)
			bounds[user] = [low, high]
			sendGuess(message.channel, user)
		} else if (user in guess) {
			if (message.content.indexOf("low") !== -1) {
				computeGuess(message.channel, user, false)
			} else if (message.content.indexOf("high") !== -1) {
				computeGuess(message.channel, user, true)
			} else if (message.content.indexOf("Correct") !== -1) {
				message.reply("Yay!")
				delete delta[user]
				delete guess[user]
			}
		}
	}
})

client.login(fs.readFileSync('tokens/' + name + '.token', 'utf8'))
