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

var opponent = ""
var delta = 0
var guess = 0

client.on('ready', () => {
	console.log(`Logged in as ${client.user.username}`)
})

function computeGuess(channel, wasHigh) {
	if (wasHigh) {
		guess -= delta
	} else {
		guess += delta
	}
	if (delta > 1) {
		delta = Math.floor(delta / 2)
	}
	sendGuess(channel)
}

function sendGuess(channel) {
	channel.send(opponent + ' ' + guess)
}

client.on('message', message => {
	if (message.mentions.users.array().includes(client.user)) {
		if (message.content.endsWith("die")) {
			client.destroy()
			process.exit(0)
		} else if (message.content.indexOf("play") !== -1) {
			var args = message.content.split(' ')
			if (args.length < 5) {
				message.reply("Usage: styx play username lowBound upBound [verbose]")
				return
			}
			opponent = args[2]
			var low = parseInt(args[3])
			var high = parseInt(args[4])
			if (args.length > 5 && args[5] === "verbose") {
				message.channel.send(opponent + " newgame " + low + " " + high)
			}
			guess = (high - low) / 2 + low
			delta = guess / 2
			sendGuess(message.channel)
		} else if (message.content.endsWith("low")) {
			computeGuess(message.channel, false)
		} else if (message.content.endsWith("high")) {
			computeGuess(message.channel, true)
		} else if (message.content.indexOf("Correct") !== -1) {
			message.reply("Yay!")
		}
	}
})

client.login(fs.readFileSync(name + '.token', 'utf8'))
