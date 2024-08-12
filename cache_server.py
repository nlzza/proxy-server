import os
import socket as sock
from constants import *
from functions import *
from urllib.request import Request, urlopen

def main():
    server = sock.socket()
    server.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
    server.bind(serv_addr)
    server.listen()
    print('Listening on ', serv_addr)

    while True:
        client, addr = server.accept()        
        request = client.recv(max_buffer).decode()
        filename, referer = filenameFromRequest(request)
        print('\nRequesting', filename, 'from', referer)

        content = getFileContent(filename, referer)
        response = getResponse(content)
        client.sendall(response.encode())
        client.close()
    server.close()

def getFileContent(filename, referer):
    try:
        fromCache = fetchFromCache(filename)
        if fromCache:
            return fromCache

        fromServer = fetchFromServer(referer + filename[1:])
        if fromServer:
            saveInCache(filename, fromServer)
            return fromServer
        return None
    except:
        return None

def fetchFromCache(filename):
    try:
        cacheFile = cachedFileName(filename)
        fin = open(cacheFile, encoding=encoding)
        content = fin.read()
        fin.close()
        print('Serving from cache', filename)
        return content
    except:
        return None

def fetchFromServer(filename):
    try:
        print('Fetching from server', filename)
        request = Request(filename)
        response = urlopen(request)
        content = response.read().decode(encoding)
        return content
    except:
        return None
        
def saveInCache(filename, content):
    cacheFile = cachedFileName(filename)
    if not os.path.exists(cacheFile):
        makeFolder(cacheFile)
    cached_file = open(cacheFile, 'w', encoding=encoding)
    cached_file.write(content)
    cached_file.close()

if __name__ == '__main__':
    main()