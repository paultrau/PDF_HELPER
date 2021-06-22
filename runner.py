# importing required modules
from typing import final
import PyPDF2
from PyPDF2 import PdfFileMerger, PdfFileReader
from os import listdir, remove, sendfile
from os.path import isfile, join
import os

from PyPDF2.generic import NullObject

NUM_FILES = 6
END_OF_FILENAME = "_2020_NYLARC_Stmt"   

#agentHandler helper class: holds the filepaths of each pdf, agent ID, file list
class agentHandler:
    def __init__(self,report,cover,stmt,id,name):
        self.report = report
        self.cover = cover
        self.stmt = stmt
        self.id = id
        self.name = name
        self.list = []
    def addFilename(string):
        list.append(string)




#generates the final name for the reports using the END_OF_FILENAME constant
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
    return final

#adds "samples/" to beginning of each string in stringList
def getPaths(stringList):
    pathList = []
    for filename in stringList:      
        path = "samples/" + filename
        pathList.append(path)
    return pathList

#creates custom agentHandler class for each agent, this holds the 3 docs and ID
def agentCreation(stringList,fileList,myPath):
    pathList = getPaths(stringList)
    agentList = []
    tempList = []
    counter = 0
    currentID = 0
    flag = True

    # Open the files and assign to agent object, add agent to agent list
    # for pathName in pathList: 
    
    print(currentID)
    while (flag):
        print("[+]Creating an agent...")
        if (fileList[counter]==NullObject):
            flag = False
            break
        currentID = pathList[counter][8:14]
        parameter = pathList[counter][8:]
        finalName = nameGen(parameter)
        cover = fileList[counter]
        counter = counter + 1
        report = fileList[counter]
        
        counter = counter + 1
        stmt = fileList[counter]
        
        counter = counter + 1
        
        if (currentID==pathList[counter][8:14]):
            alt = fileList[counter]
        else:
            counter = counter - 1
            alt = NullObject
        
        newAgent = agentHandler(cover,report,stmt,alt,pathList[counter][8:14],finalName)
        print(newAgent.id)
        agentList.append(newAgent)
    return agentList

#combines together the PDFs associated to the agent passed in
def appender(agent):
    # Read the files that you have opened
    cover = open(agent.coverPath,'rb')
    stmt = open(agent.stmtPath,'rb')
    report = open(agent.reportPath,'rb')
    print(cover)

    pdf1Reader = PyPDF2.PdfFileReader(cover)
    pdf2Reader = PyPDF2.PdfFileReader(stmt)
    pdf3Reader = PyPDF2.PdfFileReader(report)

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

#save a reports for each agent in agentList using the FINAL_PATH constant
def generateReports(agentList):
    appender(agentList[0])
    #for agent in agentList:
   #     appender(agent)

# Paramter: myPath, String representing the location of a directory, SHOULD NOT BE A SINGLE FILE
# Using the path, a sorted list of filenames is returned 
def nameListLoad(myPath):
    theList = []
    onlyfiles = [f for f in listdir(myPath) if isfile(join(myPath, f))]
    for file in onlyfiles:
        filename = os.path.basename(file)
        if (filename!=".DS_Store"):
            theList.append(filename)
    theList.sort
    return theList

#using the names parameter, a list of filenames, a list of files is returned in the order given
def fileListLoad(names):
    theList = []
    for filename in names:
        if (filename!=".DS_Store"):
            file = open("sample/"+filename)
            theList.append(file)
    return theList

#override toString function for built-in list
def printList(list):
    for obj in list:
        print(obj)

#main runner
def main():

    #Get path of file
    userInput = input("[!]Enter filepath: ")
    print("[+]...Confirmed")
    
    print("[\]Loading list of filenames...")  
    fnList = nameListLoad(userInput)
    print(fnList)
    print("[+]...Filename List Loaded!")

    
    print("[/]Loading list of files...")  
    fList = fileListLoad(fnList)
    print(fList)
    print("[+]...File List Loaded!")

    
    print("[/]Creating Agent Objects...")
    agentList = agentCreation(fnList,fList,userInput)
    print("[+]...Objects created!")

    print("[\]Printing final filenames...")
    for agent in agentList:
        print(agent.name)

    #print("[/]Creating each agent's final report...")
    #finalList = generateReports(agentList)





if __name__ == "__main__":
    main()





