#coding=utf-8
import re
import os
import copy
from fix import Fix_Generate
from net import Net_Generate

node = []
allDatas = []
signalList = []
masternode = 0
commonName = 0

def ReadFile():
    global node,allDatas,signalList
    
    InputDBC = input("Please Enter DBC file:")
    temp = InputDBC.find('.dbc')
    while(temp == -1):
        print("\fInvalid dbc file! Please input again!\r\n")
        InputDBC = input("Please Enter DBC file:")
        temp = InputDBC.find('.dbc')
    print("The input DBC file is:", InputDBC)
    dbc_fd = open(InputDBC, "r")
    #dbc_fd = open("test.dbc", "r")

    NodesPattern = re.compile(r"BU_: (.*)", re.S)
    MessagePattern = re.compile(r"BO_ (.*?) (.*?): (.*?) (.*)", re.S)
    SignalPattern = re.compile(r'''SG_ (.*?) : (.*?)\|(.*?)@.*? \((.*?),(.*?)\) \[(.*?)\|(.*?)\] "(.*?)" (.*)''', re.S)
    line = dbc_fd.readline()
    allDatas=[]
    while line:
        NodesSearched = re.search(NodesPattern, line.strip())
        if NodesSearched:
                node = NodesSearched.group(1).split(" ")
        MessagesSearched = re.search(MessagePattern, line.strip())
        if MessagesSearched:
            signalList.clear()
            Message = list(MessagesSearched.groups())
            signalList.append(Message[3])
            signalList.append(Message[1])
            signalList.append(Message[0])
            signalList.append(Message[2])
            line = dbc_fd.readline()
            MessagesSearched = re.search(MessagePattern, line.strip())
            SignalSearched = re.search(SignalPattern, line.strip())

            if not MessagesSearched:
                while SignalSearched:
                    signal = list(SignalSearched.groups())
                    signalList.append(signal)
                    line = dbc_fd.readline()
                    SignalSearched = re.search(SignalPattern, line.strip())
            c = copy.deepcopy(signalList)
            allDatas.append(c)
        else:
            line = dbc_fd.readline()
            MessagesSearched = re.search(MessagePattern, line.strip())
    dbc_fd.close()

def SelectMasterNode():
    global node,masternode
    for i in range(len(node)):
        print(str(i)+": "+node[i])
    index = input("\fPlease select your master node:")
    if int(index) < len(node):
        print("Your master node is: "+ node[int(index)])
        masternode = node[int(index)]
    else:
        print("!!!You enter the wrong index, Please try again!!!")
        SelectMasterNode()
    return 0

def ConfigName():
    global commonName
    commonName = input("\fPlease enter the common file name:")
    return

def Frame_Process(fra):
    global masternode
    if masternode == fra[0]:
        dir = 0
    else:
        dir = 1

    return


if __name__ == '__main__':
    ReadFile()
    SelectMasterNode()
    ConfigName()
    print(allDatas[0])
    Fix_Generate(allDatas, masternode, commonName)
    Net_Generate(allDatas, masternode, commonName)
    exit(0)

