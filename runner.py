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
UNI_FILE = open("NYLARC_GAAP_AUDITED_FINANCIAL_STATEMENTS_2020.pdf","rb")

#agentHandler helper class: holds the filepaths of each pdf, agent ID, file list
class agentHandler:
    def __init__(self,report,cover,stmt,alt,id,name,list):
        self.report = report
        self.cover = cover
        self.stmt = stmt
        self.id = id
        self.alt = alt
        self.name = name
        self.list = list

    def addFilename(string):
        list.append(string)

#generates the final name for the reports using the END_OF_FILENAME constant
def nameGen(filename):
    print(filename)
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

#creates a singular custom agentHandler class for each agent
def agentCreation(stringList,fileList,myPath):
    pathList = getPaths(stringList)
    agentList = []
    tempList = []
    counter = 0
    flag = True

    # Open the files and assign to agent object, add agent to agent list
    # for pathName in pathList: 
    currentID = pathList[0][8:15]
    while (counter<NUM_FILES):
        print("[+]Creating an agent...")
        print(currentID)
        data = open("text.txt")
        try:
            data = fileList[counter]
        except IndexError:
            data = NullObject
        if (data == NullObject):
            flag = False
            break

        currentID = pathList[counter][8:15]

        print("[+]Assigning Cover...")
        print(counter)
        cover = fileList[counter]
        tempList.append(pathList[counter])
        counter = counter + 1
        
        print("[+]Assigning Report...")
        print(counter)
        report = fileList[counter]
        tempList.append(pathList[counter])
        counter = counter + 1
        
        parameter = pathList[counter][8:]
        finalName = nameGen(parameter)
        
        print("[+]Assigning Statment...")
        print(counter)
        stmt = fileList[counter]
        tempList.append(pathList[counter])
        counter = counter + 1

        try:
            data = fileList[counter]
        except IndexError:
            print("[+]No Alternate Sheet Found...")
            alt = NullObject
            flag = False

        if (flag):
            if (currentID==pathList[counter][8:15]):
                print("[+]Assigning Alternate Sheet...")
                alt = fileList[counter]
                tempList.append(pathList[counter])
                counter = counter + 1
            else:
                print("[+]No Alternate Sheet Found...")
                alt = NullObject
        newAgent = agentHandler(cover,report,stmt,alt,currentID,finalName,tempList)
        print(newAgent.id)
        agentList.append(newAgent)
        tempList = []
        print(counter)
    return agentList

#combines together the PDFs associated to the agent passed in
def appender(agent):
    theFlag = True
    if (agent.alt == NullObject):
        theFlag = False
    # Read the files that you have opened
    
    #cover = agent.cover
    #stmt = agent.stmt
    #report = agent.repor

    if (theFlag):
        alt = open(agent.list[1],'rb')
        cover = open(agent.list[2],'rb')
        stmt = open(agent.list[3],'rb')
        report = open(agent.list[0],'rb')
    else:
        cover = open(agent.list[1],'rb')
        stmt = open(agent.list[2],'rb')
        report = open(agent.list[0],'rb')
    print(cover)

    pdf1Reader = PyPDF2.PdfFileReader(cover)
    pdf2Reader = PyPDF2.PdfFileReader(stmt)
    pdf3Reader = PyPDF2.PdfFileReader(report)
    if (theFlag):
        pdf4Reader = PyPDF2.PdfFileReader(alt)
    pdf5Reader = PyPDF2.PdfFileReader(UNI_FILE)

    # Create a new PdfFileWriter object which represents a blank PDF document
    pdfWriter = PyPDF2.PdfFileWriter()
    # Loop through all the pagenumbers for the three documents
    # cover
    for pageNum in range(pdf1Reader.numPages):
        pageObj = pdf1Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)
    # statement
    for pageNum in range(pdf2Reader.numPages):
        pageObj = pdf2Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)
    # death claim if needed
    if (theFlag):
        for pageNum in range(pdf4Reader.numPages):
            pageObj = pdf4Reader.getPage(pageNum)
            pdfWriter.addPage(pageObj)
    
    # report
    for pageNum in range(pdf3Reader.numPages):
        pageObj = pdf3Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)
    
    # financial statement
    for pageNum in range(pdf5Reader.numPages):
        pageObj = pdf5Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)

    # Now that you have copied all the pages in both the documents, write them into the a new document
    pdfOutputFile = open("merged/"+agent.name+".pdf", 'wb')
    pdfWriter.write(pdfOutputFile)    

#passes each agent into the appender function which creates the merged PDF
def generateReports(agentList):
    for agent in agentList:
        appender(agent)

# Paramter: myPath, String representing the location of a directory, SHOULD NOT BE A SINGLE FILE
# Using the path, a sorted list of filenames is returned 
def nameListLoad(myPath):
    theList = []
    onlyfiles = [f for f in listdir(myPath) if isfile(join(myPath, f))]
    for file in onlyfiles:
        filename = os.path.basename(file)
        if (filename!=".DS_Store"):
            theList.append(filename)
    theList.sort()
    return theList

#using the names parameter, a list of filenames, a list of files is returned in the order given
def fileListLoad(names):
    theList = []
    for filename in names:
        if (filename!=".DS_Store"):
            file = open("samples/"+filename)
            theList.append(file)
    return theList

#override toString function for built-in list
def printList(list):
    for obj in list:
        print(obj)

#python main
def main():

    #Get path of file
    userInput = input("[!]Enter filepath: ")
    print("[+]...Confirmed")
    
    #un-comment the following to take in user input for constants
    NUM_FILES = int(input("[!]Enter number of files: "))
    print("[+]...Confirmed")
    #END_OF_FILENAME = input("[!]Enter final filename suffix: ")
    #print("[+]...Confirmed")
    

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
    print(agentList)
    print("[+]...Objects created!")

    print("[\]Printing final filenames...")
    for agent in agentList:
        print(agent.name)
        print(agent.cover)

    print("[/]Creating each agent's final report...")
    finalList = generateReports(agentList)

if __name__ == "__main__":
    main()