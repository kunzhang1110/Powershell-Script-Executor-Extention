
let powershellScriptPath = localStorage.getItem('powershellScriptPath') ?? "";

window.onload = () => {
  if (powershellScriptPath) {
    document.getElementById('powershellScriptPathInput').textContent = powershellScriptPath;
    document.getElementById('powershellScriptPathInput').value = powershellScriptPath;
  }
};

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("Message from background:", message.content);
  debugger;

  if (message.type === "fromBackground" && !message.error && powershellScriptPath !== "") {
    localStorage.setItem('powershellScriptPath', powershellScriptPath);
  }
  setLoadingSpinner(false);
});

document.getElementById("executeScript").addEventListener("click", () => {
  try {
    setLoadingSpinner(true);


    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const currentUrl = tabs[0].url;
      powershellScriptPath = document.getElementById(
        "powershellScriptPathInput"
      ).value;


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
    setLoadingSpinner(false);
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

function setLoadingSpinner(shouldSpinnerShow) {
  const loadingSpinner = document.getElementById("loadingSpinner");
  const inputGroup = document.getElementById("inputGroup");
  if (shouldSpinnerShow) {
    loadingSpinner.style.display = "block";
    inputGroup.style.visibility = "hidden";
  } else {
    loadingSpinner.style.display = "none";
    inputGroup.style.visibility = "visible";
  }

}