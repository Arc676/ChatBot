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

const MTG = require('mtgsdk')
const Discord = require('discord.js')

const client = new Discord.Client()

var name = "titania"
var resultLimit = 10

client.on('ready', () => {
	console.log(`Logged in as ${client.user.username}`)
})

const properties = [
	[
		"name",
		"manaCost"
	],
	[
		"rarity",
		"types"
	],
	[
		"text"
	],
	[
		"power",
		"toughness"
	]
]
function printCard(message, card) {
	var text = ""
	for (var i = 0; i < properties.length; i++) {
		for (var j = 0; j < properties[i].length; j++) {
			if (properties[i][j] in card) {
				text += card[properties[i][j]]
				if (j + 1 < properties[i].length) {
					text += "/"
				}
			}
		}
		text += "\n"
	}
	message.reply(text)
}

function getQueryProperties(query) {
	var properties = {}
	for (var i = 0; i < query.length; i++) {
		const prop = query[i].split("=")
		properties[prop[0]] = prop[1].replace(/\+/g, ' ')
	}
	return properties
}

client.on('message', message => {
	if (message.content.startsWith(name + " ")) {
		if (message.content.endsWith(" die")) {
			client.destroy()
			process.exit(0)
		} else if (message.content.indexOf(" limit ") !== -1) {
			const args = message.content.split(" ")
			resultLimit = parseInt(args[2])
		}
		return
	}
	const startIndex = message.content.indexOf("[[")
	const endIndex = message.content.indexOf("]]")
	if (startIndex !== -1 && endIndex !== -1) {
		const query = message.content.substring(startIndex + 2, endIndex).split(" ")
		if (query.length === 0) {
			return
		}
		if (message.content.startsWith("set")) {
			//const properties = getQueryProperties(query.splice(1))
			message.reply("Set searching coming soon!")
		} else {
			var printText = true
			var printImage = false
			var debug = false
			if (message.content.startsWith("debug")) {
				debug = true
				printText = false
			} else if (message.content.startsWith("image")) {
				printImage = true
				printText = false
			} else if (message.content.startsWith("combo")) {
				printImage = true
			}
			const properties = getQueryProperties(query)
			if (properties === undefined) {
				message.reply("Sorry, your query failed")
				return
			}
			MTG.card.where(properties).then(cards => {
				distinct = {}
				found = 0
				for (var i = 0; i < cards.length; i++) {
					if (!(cards[i].name in distinct)) {
						distinct[cards[i].name] = cards[i]
						found++
					}
				}
				message.reply("Found " + found + " distinct card(s)")
				if (found > resultLimit) {
					message.reply("Result count exceeds limit. Aborting.")
					return
				}
				for (let card in distinct) {
					if (printText) {
						printCard(message, distinct[card])
					}
					if (printImage) {
						message.reply(distinct[card]['imageUrl'])
					}
					if (debug) {
						console.log(distinct[card])
					}
				}
				message.reply("End of search results")
			})
		}
	}

})

client.login(fs.readFileSync('tokens/' + name + '.token', 'utf8'))
