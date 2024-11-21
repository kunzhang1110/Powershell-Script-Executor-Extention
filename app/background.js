let port;

// Listen for messages from popup.js and forward them to the native host
chrome.runtime.onMessage.addListener((msgFromPopup, sender, sendResponse) => {
  if (msgFromPopup.type === "fromPopup") {
    // if port is not connected, connect to the native host
    if (!port) connectToNativeHost(); 
    
    if (port) {
      port.postMessage(msgFromPopup.content);
    } else {
      // if port connection fails, send a message to the popup.js
      sendResponse({
        type: "fromBackground",
        content: "Port is not connected.",
      });
    }
  }
});

function connectToNativeHost() {
  port = chrome.runtime.connectNative("kunzhang1110.powershellrunner");

  // Listen for message from native host
  port.onMessage.addListener((respFromNativeHost) => {
    console.log("Received from NativeMessagingHost: " + respFromNativeHost);
    let hasError = respFromNativeHost.startsWith("Error");
    let msgToPopup = {
      type: "fromBackground",
      content: respFromNativeHost,
      hasError,
    };
    chrome.runtime.sendMessage(msgToPopup);
  });

  // Listen for disconnection events
  port.onDisconnect.addListener(() => {
    console.log(`Port disconnected due to an error: ${port.error?.message}`);
    port = null;
  });
}
