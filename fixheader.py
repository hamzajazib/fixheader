__author__ = "hamzajazib"
__version__ = "1.0"

import sys
import argparse
from pathlib import Path

def readFile(filePath):
    try:
        with filePath.open('rb') as f:
            data = f.read()
    except IOError as e:
        print(e)
        sys.exit()
    return data.hex().upper()

def writeFile(filePath, fileData):
    try:
        newFilePath = Path(filePath.stem + "_fixed_header" + filePath.suffix)
        with newFilePath.open('wb') as f:
            f.write(bytes.fromhex(fileData))
            print("saved as " + str(newFilePath.resolve()))
    except IOError as e:
        print(e)
        sys.exit()

def isPNG(fileData):
    features = ['504E47','49484452','49444154','49454E44'] #['PNG','IHDR','IDAT','IEND']
    for feature in features:
        if feature in fileData:
            return True
    return False

def fixHeader(header,fileData):
    fileHeader = fileData[0:len(header)]
    if fileHeader != header:
        fileData = header + fileData[len(header):]
        print(f'Fixed Header {fileHeader} to {header}')
        return fileData
    else:
        print("Header unchanged")
        return
    
def fix(fileData):
    if isPNG(fileData):
        print("File recognized as possible PNG")
        headerPNG = "89504E470D0A1A0A"
        fileData = fixHeader(headerPNG, fileData)
        return fileData
    else:
        print("Unknown file format")
        return

def main():
    parser = argparse.ArgumentParser(description = "Fix file header signatures for file types (PNG)")
    parser.add_argument('-i', '--input', metavar = 'file', help = "Input file")
    args = parser.parse_args()
    if args.input:
        inputFilePath = Path(args.input)
        if inputFilePath.exists():
            fileData = readFile(inputFilePath)
            fileData = fix(fileData)
            if fileData:
                writeFile(inputFilePath,fileData)
        else:
            print("File doesn't exist")
    else:
        parser.print_help()

main()
