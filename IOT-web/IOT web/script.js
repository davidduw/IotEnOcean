// Create a client instance
client = new Paho.MQTT.Client("178.32.217.100", Number("61614"), "clientId-Blblbblblblbl");

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({onSuccess:onConnect});


// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  client.subscribe("#");
  message = new Paho.MQTT.Message("Hello");
  message.destinationName = "World";
  client.send(message);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}

// called when a message arrives
function onMessageArrived(message) {
	console.log("onMessageArrived:"+message.payloadString);
	console.log("Topic:"+message.destinationName);
	switch(message.destinationName) {
		case "2690016":
			switch(message.payloadString){
				case "Brown0":
					document.getElementById("switch").value = "Marron 0";
					break;
				case "BrownI":
					document.getElementById("switch").value = "Marron I";
					break;
				case "White0":
					document.getElementById("switch").value = "Blanc 0";
					break;
				case "WhiteI":
					document.getElementById("switch").value = "Blanc I";
					break;
				case "B0W0":
					document.getElementById("switch").value = "Marron/Blanc 0";
					break;
				case "BIWI":
					document.getElementById("switch").value = "Marron/Blanc I";
					break;
				case "BIW0":
					document.getElementById("switch").value = "Marron I/Blanc 0";
					break;
				case "B0WI":
					document.getElementById("switch").value = "Marron 0/Blanc I";
					break;
				case "Neutral":
					document.getElementById("switch").value = document.getElementById("switch").value+" (relaché)";
					break;
				default:
					document.getElementById("switch").value = "Action non reconnue";
			}
			break;
		case "25203027":
			switch(message.payloadString){
				case "close":
					document.getElementById("door").value = "Fermé";
					document.getElementById("doorImg").src = "close.jpg";
					break;
				case "open":
					document.getElementById("door").value = "Ouvert";
					document.getElementById("doorImg").src = "open.jpg";
					break;
				default:
			}
			break;
		case "26374959":
			document.getElementById("prise").value = message.payloadString;
			break;
		case "25307177":
			document.getElementById("temp").value = message.payloadString;
			break;
		default:
		
	}		
}