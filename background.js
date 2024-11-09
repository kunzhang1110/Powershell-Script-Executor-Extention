/*
On startup, connect to the "ping_pong" app.
*/
let port = chrome.runtime.connectNative("kunzhang1110.powershellrunner");

port.onMessage.addListener((response) => {
  console.log("Received: " + response);
  chrome.runtime.sendMessage({ type: "fromBackground", content: response });
});

port.onDisconnect.addListener((port) => {
  if (port.error) {
    console.log(`Disconnected due to an error: ${port.error.message}`);
  } else {
    console.log(`Disconnected`, port);
  }
});

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.type === "fromPopup") {
    port.postMessage(message.content);
  }
});
