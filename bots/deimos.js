//MIT License

//Copyright (c) 2018 Arc676/Alessandro Vinciguerra

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
const cp = require('child_process')

var name = "deimos"
var runningScripts = 0

client.on('ready', () => {
	console.log(`Logged in as ${client.user.username}`)
})

function evaluate(data) {
	runningScripts++
	let sNum = runningScripts
	let sFile = "script" + sNum
	let iFile = "input" + sNum
	let cmd = "./vongsprache scriptX < inputX".replace(/X/g, sNum)
	runningScripts--

	let fds = fs.openSync(sFile, "w")
	fs.writeSync(fds, data.script)
	fs.close(fds)

	let fdi = fs.openSync(iFile, "w")
	fs.writeSync(fdi, data.input)
	fs.close(fdi)

	var ret = ""
	try {
		ret = cp.execSync(cmd).toString()
	} catch (e) {
		ret = e.status + ": " + e.stderr.toString()
	}
	fs.unlink(sFile)
	fs.unlink(iFile)
	return ret
}

client.on('message', message => {
	if (message.author.bot) return
	if (message.content.startsWith(name)) {
		if (message.content.endsWith(' die')) {
			client.destroy()
			process.exit(0)
		} else {
			try {
				var data = {}
				let blocks = message.content.split(/```/)
				data.script = blocks[1].trim()
				data.input = blocks[3].trim() + "\n"
				let resp = evaluate(data)
				message.reply(resp)
			} catch (e) {
				message.reply("Malformed request")
			}
		}
	}
})

client.login(fs.readFileSync('tokens/' + name + '.token', 'utf8'))
