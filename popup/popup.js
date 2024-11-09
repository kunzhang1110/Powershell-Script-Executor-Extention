window.onload = function() {
  const powershellScriptPath = localStorage.getItem('powershellScriptPath');
  if (powershellScriptPath) {
    document.getElementById('powershellScriptPathInput').textContent = powershellScriptPath;
    document.getElementById('powershellScriptPathInput').value = powershellScriptPath;
  }
};

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.type === "fromBackground") {
    console.log("Response from background:", message.content);
    // document.getElementById("loadingSpinner").style.display = "none";
    // document.getElementById("inputGroup").style.display = "block";

    document.getElementById("loadingSpinner").style.display = "none";
    document.getElementById("inputGroup").style.visibility = "visible";
  }
});

document.getElementById("executeScript").addEventListener("click", () => {
  try {
    // document.getElementById("loadingSpinner").style.display = "block";
    // document.getElementById("inputGroup").style.display = "none";
  
    document.getElementById("loadingSpinner").style.display = "block";
    document.getElementById("inputGroup").style.visibility = "hidden";

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const currentUrl = tabs[0].url;
      const powershellScriptPath = document.getElementById(
        "powershellScriptPathInput"
      ).value;

      localStorage.setItem('powershellScriptPath', powershellScriptPath);

      const content = {
        url: currentUrl,
        powershellScriptPath: powershellScriptPath ?? "",
      };

      chrome.runtime.sendMessage(
        {
          type: "fromPopup",
          content: content,
        }
      );
    });
  } catch (error) {
    console.error("Error:", error);
  }
});

document.getElementById("restartBackground").addEventListener("click", () => {
  try {
    chrome.runtime.reload(); // Reload the extension, which restarts background.js
    console.log("Background script is restarting...");
  } catch (error) {
    console.error("Error restarting the background script:", error);
  }
});
