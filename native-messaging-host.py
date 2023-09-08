#!/usr/bin/env -S python3 -u

import sys
import json
import struct
import time
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)
incoming_log = logging.getLogger("firefox")
outgoing_log = logging.getLogger("python")

def getMessage():
    rawLength = sys.stdin.buffer.read(4)
    if len(rawLength) == 0:
        sys.exit(0)
    messageLength = struct.unpack('@I', rawLength)[0]
    message = sys.stdin.buffer.read(messageLength).decode('utf-8')
    incoming_log.debug(message)
    return json.loads(message)

def encodeMessage(messageContent):
    encodedContent = json.dumps(messageContent, separators=(',', ':')).encode('utf-8')
    encodedLength = struct.pack('@I', len(encodedContent))
    return {'length': encodedLength, 'content': encodedContent}

def sendMessage(msg):
    outgoing_log.debug(msg)
    encodedMessage = encodeMessage(msg)
    sys.stdout.buffer.write(encodedMessage['length'])
    sys.stdout.buffer.write(encodedMessage['content'])
    sys.stdout.buffer.flush()

def getTabInfo(tabId):
    sendMessage({"command": "tab_info", "type": "request", "tabId": tabId})
    tab_resp = getMessage()
    if (data := tab_resp["data"]):
        if data["audible"]:
            incoming_log.info(json.dumps(tab_resp, indent=2))

def getWindowsAndTabs():
    for i in range(5000):
        getTabInfo(i)
        time.sleep(0.01)


while True:
    receivedMessage = getMessage()

    if receivedMessage == "get_tabs":
        windowsAndTabs = getWindowsAndTabs()
        sendMessage(windowsAndTabs)
    if receivedMessage == "tab_info":
        windowsAndTabs = getWindowsAndTabs()
        sendMessage(windowsAndTabs)
    elif receivedMessage:
        sendMessage("hey back")

