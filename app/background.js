let port, isConnected = false;

function connect() {
  port = chrome.runtime.connectNative("kunzhang1110.powershellrunner");
  isConnected = true;
}

connect();

port.onMessage.addListener((message) => {
  console.log("Received from NativeMessagingHost: " + message);
  let forwardMessage = { type: "fromBackground", content: message, error: false };
  if (message.startsWith("Error")) {
    forwardMessage.error = true;
  }
  chrome.runtime.sendMessage(forwardMessage);
});

port.onDisconnect.addListener((port) => {
  if (port.error) {
    console.log(`Port disconnected due to an error: ${port.error.message}`);
  } else {
    console.log(`Port Disconnected`);
  }
  isConnected = false;
});

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if ((message.type === "fromPopup") && isConnected) {
    port.postMessage(message.content);
  } else {
    sendResponse({ type: "fromBackground", content: "Port is not connected." });
  }

});
