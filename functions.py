import os
from constants import *

def filenameFromRequest(request):
    headers = request.split('\n')
    top_header = headers[0].split()
    filename = top_header[1]

    if filename == '/':
        return indexHtml, pathPrefix
    if filterFile(filename):
        return blockHtml, pathPrefix
    return filename, 'https://'

def getResponse(content):
    return successHeader + content if content else errorHeader

def makeFolder(folder):
    folder = folder.split("\\")[:-1]
    path = ''
    for subFolder in folder:
        path += subFolder
        if not os.path.exists(path):
            os.makedirs(path)
        path += '\\'

def cachedFileName(filename):
    return 'cache' + filename

def filterFile(filename):
    for file in open(blockedFiles, 'r'):
        if filename == file.rstrip():
            return True
    return False