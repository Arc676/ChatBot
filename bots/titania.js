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

client.on('ready', () => {
	console.log(`Logged in as ${client.user.username}`)
})

function printCard(message, card) {
//	message.reply(card.name)
	console.log(card.name)
}

function getQueryProperties(query) {
	return { supertypes: 'legendary', subtypes: 'goblin' }
}

client.on('message', message => {
	if (message.content === name + " die") {
		client.destroy()
		process.exit(0)
	}
	const startIndex = message.content.indexOf("[[")
	const endIndex = message.content.indexOf("]]")
	if (startIndex !== -1 && endIndex !== -1) {
		const query = message.content.substr(startIndex + 2, endIndex).split(" ")
		if (query.length === 0) {
			return
		}
		if (query[0] === "set") {
			//const properties = getQueryProperties(query.splice(1))
			message.reply("Set searching coming soon!")
		} else {
			const properties = getQueryProperties(query)
			if (properties === undefined) {
				message.reply("Sorry, your query failed")
				return
			}
			MTG.card.where(properties).then(cards => {
				message.reply("Found " + cards.length + " cards (including duplicates)")
				alreadyPrinted = []
				for (var i = 0; i < cards.length; i++) {
					if (!alreadyPrinted.includes(cards[i].name)) {
						printCard(message, cards[i])
						alreadyPrinted.push(cards[i].name)
					}
				}
				console.log(alreadyPrinted)
			})
		}
	}

})

client.login(fs.readFileSync('tokens/' + name + '.token', 'utf8'))
