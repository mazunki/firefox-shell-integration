
let mazport = browser.runtime.connectNative("tech.mazunki.ff_integration");

mazport.onMessage.addListener((request) => {
	console.info(request);
    if (request.command === "tab_info" && request.type === "request") {
		browser.tabs.get(request.tabId).then(
			(tabInfo) => { mazport.postMessage({command: "tab_info", type: "response", tabId: request.tabId, data: tabInfo}) },
			(err) => { mazport.postMessage({command: "tab_info", type: "response", tabId: request.tabId, data: null}) }
		);
    }
});

mazport.onDisconnect.addListener( (port) => {
	console.error(port.sender, port.error);
});


