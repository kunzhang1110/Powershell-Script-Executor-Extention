import sys
import json
import struct
import subprocess

def getMessage():
    rawLength = sys.stdin.buffer.read(4)
    if len(rawLength) == 0:
        sys.exit(0)
    messageLength = struct.unpack('@I', rawLength)[0]
    message = sys.stdin.buffer.read(messageLength).decode('utf-8')
    return json.loads(message)


def encodeMessage(messageContent):
    encodedContent = json.dumps(
        messageContent, separators=(',', ':')).encode('utf-8')
    encodedLength = struct.pack('@I', len(encodedContent))
    return {'length': encodedLength, 'content': encodedContent}


def sendMessage(encodedMessage):
    sys.stdout.buffer.write(encodedMessage['length'])
    sys.stdout.buffer.write(encodedMessage['content'])
    sys.stdout.buffer.flush()


def runPowerShellWithUrl(url,powershellScriptPath):
    command = ["powershell", "-ExecutionPolicy", "Bypass", "-File", powershellScriptPath, "-url", url]
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # DEVNULL is crucial
    except Exception as e:
        raise Exception("Error: " + str(e))
    pass
       

while True:
    try:
        receivedMessage = getMessage() 
        url = receivedMessage["url"]
        powershellScriptPath = receivedMessage.get("powershellScriptPath", "C:\\GitHub\\Sandbox\\powershell-script-executor\\NativeMessageHost\\run.ps1")
        
        if url:
            runPowerShellWithUrl(url,powershellScriptPath)
            sendMessage(encodeMessage(url))
    except Exception as e:
        sendMessage(encodeMessage("Error: " + str(e)))
        break
    
