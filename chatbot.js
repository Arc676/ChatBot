const Discord = require('discord.js');
const client = new Discord.Client();

var callAndResponse = [
	["I love you", "I know"],
	["ping", "pong"],
	["This is madness!", "Madness?  **THIS IS SPARTA!**"],
	["There isn't enough road", "Where we're going, we don't need roads."],
	["May the force be with you", "And also with you"],
	["Is this Tony Stank\\?", "Yes, this is the Tony Stank"],
	["[wW]here [ia][sr]e? .+\\?", "Somewhere, over the rainbow"],
	["[wW]hat is .+", "42"],
	["Why did the chicken cross the road\?", "To get to the other side"],
	["LICENSE", "MIT License at https://github.com/Arc676/ChatBot"],
	["Watcha doin\\?", "Eatin' chocolate"],
	["Whered'ya get it\\?", "A dog dropped it!"],
	["This isn't your average, everyday (.+)", "This is **ADVANCED $**"]
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
	
	//Check for basic commands first (switch is supposedly faster, so leave the for-loop for later)
	//Checks for commands (Add chatbot + commands support later)
	switch (msg) {
	case "chatbothelp":
		return "Recognized commands:\n\tping\n\tchatbot\n\tchatbothelp\n\tchatbotgoaway\n\tchatbotstay\n\t(various movie quotes)"
	default:
		break;
	}
	
	//Loop through array and get the appropriate response to the call
	for (var i = 0; i < callAndResponse.length; i++){
		var regexp = new RegExp(callAndResponse[i][0]);
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
