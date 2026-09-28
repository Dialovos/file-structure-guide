// Runs inside matched pages. Treat page data as untrusted.
chrome.runtime.sendMessage({ type: MSG.GET_COUNT }).then((reply) => {
  console.debug("extension count:", reply?.count);
});
