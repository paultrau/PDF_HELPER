# importing required modules
from typing import final
import PyPDF2
from PyPDF2 import PdfFileMerger, PdfFileReader
from os import listdir, remove
from os.path import isfile, join
import os

NUM_FILES = 6
END_OF_FILENAME = "_2020_NYLARC_Stmt"   

class agentHandler:
    def __init__(self,report,cover,stmt,id,name):
        self.report = report
        self.cover = cover
        self.stmt = stmt
        self.id = id
        self.name = name



def nameGen(filename):
    check = filename[0]
    final = ""
    counter = 0
    numScores = 0
    
    while (numScores < 3):
        while True:
            final = final + check
            counter = counter + 1
            check = filename[counter]
            if(check=="_"):
                break
        numScores = numScores + 1
    final = final + END_OF_FILENAME
    print(final)
    return final


#creates custom agentHandler class for each agent, this holds the 3 docs and ID
def agentCreation(stringList,myPath):
    pathList = []
    agentList = []
    for filename in stringList:      
        path = "samples/" + filename
        pathList.append(path)
        print(path)   
    # Open the files and assign to agent object, add agent to agent list
    for i in range(0,NUM_FILES+1,3):
        print("Creating an agent...")
        parameter = pathList[i][8:]
        print(parameter)
        finalName = nameGen(parameter)
        print(finalName)
        report = open(pathList[i], 'rb')
        i2 = i+2
        print(report)
        cover = open(pathList[i+1], 'rb')
        stmt = open(pathList[i2],'rb')
        newAgent = agentHandler(cover,report,stmt,pathList[i][7:13],finalName)
        print(newAgent)
        agentList.append(newAgent)
    return agentList

def appender(agent):
    # Read the files that you have opened
    pdf1Reader = PyPDF2.PdfFileReader(agent.cover)
    pdf2Reader = PyPDF2.PdfFileReader(agent.stmt)
    pdf3Reader = PyPDF2.PdfFileReader(agent.report)

    # Create a new PdfFileWriter object which represents a blank PDF document
    pdfWriter = PyPDF2.PdfFileWriter()

    # Loop through all the pagenumbers for the three documents
    for pageNum in range(pdf1Reader.numPages):
        pageObj = pdf1Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)
    for pageNum in range(pdf2Reader.numPages):
        pageObj = pdf2Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)
    for pageNum in range(pdf3Reader.numPages):
        pageObj = pdf3Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)

    # Now that you have copied all the pages in both the documents, write them into the a new document
    pdfOutputFile = open('MergedFiles.pdf', 'wb')
    pdfWriter.write(pdfOutputFile)    
    
    print("List Loaded...")

def generateReports(agentList):
    for agent in agentList:
        appender(agent)

def listLoad(myPath):
    theList = []
    onlyfiles = [f for f in listdir(myPath) if isfile(join(myPath, f))]
    for file in onlyfiles:
        filename = os.path.basename(file)
        theList.append(filename)
    theList.remove(".DS_Store")
    return theList;    

def printList(list):
    for obj in list:
        print(obj)

#main runner
def main():
    userInput = input("[!]Enter filepath: ")
    print("[+]...Confirmed")
    
    print("[\]Loading list of filenames...")  
    fnList = listLoad(userInput)
    print(fnList)
    print("[+]...Filename List Loaded!")
    
    print("[/]Creating Agent Objects...")
    agentList = agentCreation(fnList,userInput)
    print("[+]...Objects created!")

    print("[\]Printing final filenames...")
    for agent in agentList:
        print(agent.name)

    print("[/]Creating each agent's final report...")
    #finalList = generateReports(agentList)





if __name__ == "__main__":
    main()





