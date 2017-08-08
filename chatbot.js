const Discord = require('discord.js');
const client = new Discord.Client();

var callAndResponse = [
	["I love you", "I know"],
	["ping", "pong"],
	["This is madness!", "Madness?  **THIS IS SPARTA!**"],
];

var shouldLeave = false;

//function sleep(ms){
//	return new Promise(resolve => setTimeout(resolve, ms));
//}

client.on('ready', () => {
	console.log(`I am ready! (${client.user.username})`);
//	client.sendMessage("ChatBot has arrived!");
});

function getReply(msg){
	
	//Loop through array and get the appropriate response to the call
	for (var i = 0; i < callAndResponse.length; i++){
		if (msg == callAndResponse[i][0]){
			return callAndResponse[i][1];
		}	
	}
	
	//Checks for commands (Add chatbot + commands support later)
	switch (msg) {
	case "chatbothelp":
		return "Recognized commands:\n\tping\n\tchatbot\n\tchatbothelp\n\tchatbotgoaway\n\tchatbotstay"
	default:
		return "";
	}
}

client.on('message', message => {
	if (message.content === 'chatbotgoaway') { //Makes chatbot leave
		if (shouldLeave) {
			message.reply('OK :(');
			//await sleep(1000);
			client.destroy();
			process.exit(0);
		} else {
			message.reply('Repeat command to confirm');
			shouldLeave = true
		}
	} else if (message.content === 'chatbotstay') { //Cancels leave
		message.reply('OK I\'ll stay');
		shouldLeave = false
	} else { //Runs commands and performs call and response
		var response = getReply(message.content);
		if (response !== "") {
			message.reply(response);
		}
	}
});

client.login('MzQ0NDMwNzk0NzYyMzU0Njg5.DGsnyA.J9vVgXAqO7YRz4rZGOyAmu9dTFE');
