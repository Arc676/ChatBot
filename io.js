const Discord = require('discord.js');
const client = new Discord.Client();

var callAndResponse = [
	["I love you", "I know"],
	["ping", "pong"],
	["This is madness!", "Madness?  **THIS IS SPARTA!**"],
	["There isn't enough road", "Where we're going, we don't need roads."],
	["May the force be with you", "And also with you"],
	["Is this Tony Stank\\?", "Yes, this is the Tony Stank"],
	["where [ia][sr]e? .+\\?", "Somewhere, over the rainbow"],
	["what is .+", "42"],
	["Why did the chicken cross the road\?", "To get to the other side"],
	["LICENSE", "MIT License at https://github.com/Arc676/ChatBot"],
	["Watcha doin\\?", "Eatin' chocolate"],
	["Whered'ya get it\\?", "A dog dropped it!"],
	["This isn't your average, everyday (.+)", "This is **ADVANCED** $"],
	["How many (\\w+)", "ALL THE $"],
	["thank.+\\Wio\\W|thank.+\\Wio$", "You are very welcome"]
];

var name = "io"
var active = true;

client.on('ready', () => {
	console.log(`Logged in as ${client.user.username}`);
//	client.sendMessage("ChatBot has arrived!");
});

function getReply(msg){
	
	//Loop through array and get the appropriate response to the call
	for (var i = 0; i < callAndResponse.length; i++){
		var regexp = new RegExp(callAndResponse[i][0], 'i');
		if (regexp.test(msg)){
			response = callAndResponse[i][1];
			if (callAndResponse[i][0].indexOf("(") !== -1) {
				var match = regexp.exec(msg);
				response = response.replace("$", match[1]);
			}
			return response;
		}
	}
	
	return "";
}

client.on('message', message => {
	if (message.author.bot) return;
	if (!active) {
		if (message.content === 'Io come back') {
			message.reply("I'm back");
			active = true;
		}
		return;
	}
	if (message.content === name) {
		message.reply("Hi there!");
	} else if (message.content.startsWith(name + ", ")) {
		if (message.content.endsWith(' go away')) { //Makes chatbot leave
			message.reply('OK :(');
			active = false
		} else if (message.content.endsWith(' help')) {
			message.reply("Recognized commands:\n\thelp\n\tgo away\n\tcome back\n\tdie\n\trtfm\n\t(various movie quotes)");
		} else if (message.content.endsWith(' die')) {
			client.destroy();
			process.exit(0);
		} else if (message.content.endsWith(' rtfm')) {
			message.reply("Follow your own advice: https://discord.js.org/#/docs/main/stable/general/welcome");
		} else {
			message.reply("Yes?");
		}
	} else { //Runs commands and performs call and response
		var response = getReply(message.content);
		if (response !== "") {
			message.reply(response);
		}
	}
});

client.login('MzQ0NDMwNzk0NzYyMzU0Njg5.DGsnyA.J9vVgXAqO7YRz4rZGOyAmu9dTFE');
