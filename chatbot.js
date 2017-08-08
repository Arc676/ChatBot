const Discord = require('discord.js');
const client = new Discord.Client();

var shouldLeave = false

//function sleep(ms){
//	return new Promise(resolve => setTimeout(resolve, ms));
//}

client.on('ready', () => {
	console.log(`I am ready! (${client.user.username})`);
//	client.sendMessage("ChatBot has arrived!");
});

function getReply(msg){
	switch (msg) {
	case "ping":
		return "pong";
	case "chatbot":
		return "You rang?";
	case "chatbothelp":
		return "Recognized commands:\n\tping\n\tchatbot\n\tchatbothelp\n\tchatbotgoaway\n\tchatbotstay"
	case "I love you":
		return "I know";
	default:
		return "";
	}
}

client.on('message', message => {
	if (message.content === 'chatbotgoaway') {
		if (shouldLeave) {
			message.reply('OK :(');
			//await sleep(1000);
			client.destroy();
			process.exit(0);
		} else {
			message.reply('Repeat command to confirm');
			shouldLeave = true
		}
	} else if (message.content === 'chatbotstay') {
		message.reply('OK I\'ll stay');
		shouldLeave = false
	} else {
		var response = getReply(message.content);
		if (response !== "") {
			message.reply(response);
		}
	}
});

client.login('MzQ0NDMwNzk0NzYyMzU0Njg5.DGsnyA.J9vVgXAqO7YRz4rZGOyAmu9dTFE');
