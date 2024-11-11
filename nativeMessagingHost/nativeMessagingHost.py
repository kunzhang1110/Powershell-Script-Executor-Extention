import sys
import json
import struct
import subprocess

defaultPowershellScriptPath = "C:\\Users\\KZhang\\Documents\\GitHub\\Powershell-Script-Executor-Extention\\nativeMessagingHost\\nativeMessagingHost.py"

def getMessage() -> dict:
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


def runPowerShellWithUrl(url, powershellScriptPath):
    command = ["powershell", "-ExecutionPolicy", "Bypass",
               "-File", powershellScriptPath, "-url", url]
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)  # DEVNULL is crucial
    except Exception as e:
        raise Exception(str(e))
    pass


while True:
    try:
        receivedMessage = getMessage()
        url = receivedMessage["url"]
        powershellScriptPath = receivedMessage.get(
            "powershellScriptPath", "")
        if powershellScriptPath == "":
            powershellScriptPath = defaultPowershellScriptPath
        if url:
            runPowerShellWithUrl(url, powershellScriptPath)
            sendMessage(encodeMessage(url))
        else:
            sendMessage(encodeMessage("Error: Invalid URL"))
    except Exception as e:
        sendMessage(encodeMessage("Error: " + str(e)))
