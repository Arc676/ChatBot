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

client.on('ready', () => {
	console.log(`Logged in as ${client.user.username}`)
})

client.on('message', message => {
	if (message.content.startsWith(name + ' ')) {
		if (message.content.endsWith(' die')) {
			client.destroy()
			process.exit(0)
		}
		var index = name.length + 1
		const colon = message.content.indexOf(':')
		if (colon !== -1) {
			index = colon + 1
		}
		const options = message.content.substring(index).split(" or ")
		message.reply(options[Math.floor(Math.random() * options.length)])
	}
})

client.login(fs.readFileSync('tokens/' + name + '.token', 'utf8'))
