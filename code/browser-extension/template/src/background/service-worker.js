// Runs on demand and may be stopped at any time. Keep no state in variables.
importScripts("../shared/messages.js");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message?.type === MSG.GET_COUNT) {
    chrome.storage.local.get({ count: 0 }).then(({ count }) => sendResponse({ count }));
    return true; // keep the channel open for the async response
  }
});
