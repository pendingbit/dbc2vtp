# coding=UTF-8
import os
import argparse
import xlsxwriter as xw
import pandas as pd
import re
import openpyxl
from fix import CreateFix
from net import CreateNet
from pri import CreatePri
from header import CreateH


def decode(dbc):
    temp = []

    for str1 in dbc:
        ans = {}
        # 报文帧
        if str1.startswith('BO_'):
            list1 = re.split(" |: |\n",str1)
            ans['message_id'],ans['message_name'],ans['message_size'],ans['transmitter'] = list1[1],list1[2],list1[3],list1[4]
            for str2 in dbc:
                if str2.startswith('BA_ "GenMsgSendType" BO_ '+ans['message_id']):
                    list2 = re.split(" ",str2)
                    ans['SendType'] = list2[-1][:-2]
                if str2.startswith('BA_ "GenMsgCycleTime" BO_ '+ans['message_id']):
                    list2 = re.split(" ",str2)
                    ans['CycleTime'] = list2[-1][:-2]
            temp.append(ans)
        # 信号帧
        elif str1.startswith(' SG_'):
            str1 = str1[5:] # 去掉" SG_ ",共5个字符
            ans['empty1'],ans['empty2'],ans['empty3'],ans['empty4'],ans['empty5'],ans['empty6'] = None,None,None,None,None,None

            sub = ':'
            spt = [sub.start() for sub in re.finditer(sub , str1)]
            ans['signal_name'],ans['multiplexer_indicator'] = re.split(" ",str1[0:spt[0]])[0], re.split(" ",str1[0:spt[0]])[1]
            str1 = str1[spt[0]+2:]

            sub = '@'
            spt = [sub.start() for sub in re.finditer(sub , str1)]
            ans['start_bit'],ans['signal_size'],ans['byte_order'],ans['value_type'] = str1[0: str1.find('|',0,spt[0])], str1[str1.find('|',0,spt[0])+1:spt[0]], str1[spt[0]+1], str1[spt[0]+2]
            if ans['byte_order'] == '0':
                ans['byte_order'] = 'intel'
            elif ans['byte_order'] == '1':
                ans['byte_order'] = 'motorola'
            if ans['value_type'] == '+':
                ans['value_type'] = '无符号数'
            elif ans['value_type'] == '-':
                ans['value_type'] = '有符号数'
            str1 = str1[spt[0]+4:]

            spt = str1.find(' ')
            ans['factor'],ans['offset'] = re.split(",",str1[1:spt-1])[0], re.split(",",str1[1:spt-1])[1]
            str1 = str1[spt+1:]

            sub = ']'
            spt = [sub.start() for sub in re.finditer(sub , str1)]
            ans['minimum'],ans['maximum'] = str1[1: str1.find('|',0,spt[0])], str1[str1.find('|',0,spt[0])+1:str1.find(']')]
            str1 = str1[spt[0]+2:]
            ans['unit'],ans['receiver'] = str1[0:str1.find(' ')], str1[str1.find(' ')+1:-2]

            temp.append(ans)

    return temp


def ReadFile(dbc):
    dbc_lines = []

    temp = dbc.find('.dbc')
    while(temp == -1):
        print("\fInvalid dbc file! Please input again!\r\n")
        dbc = input("Please Enter DBC file:")
        temp = dbc.find('.dbc')
    print("The input DBC file is:", dbc)

    with open(dbc, encoding='gbk') as f:
        dbc_lines = f.readlines()

    return dbc_lines


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='将指定dbc文件转换为vtp所用的fix，net配置文件')
    parser.add_argument('dbc_file', type=str,help='完整DBC文件路径')
    parser.add_argument('main_node', type=str, help='控制器对应网络节点')
    args = parser.parse_args()
    dbc_file = args.dbc_file
    m_node = args.main_node

    dbc_string = ReadFile(dbc_file)
    dbc_data = decode(dbc_string)
    
    CreateFix(dbc_data,m_node)
    CreateNet(dbc_data,m_node)
    CreatePri(dbc_data,m_node)
    CreateH(dbc_data,m_node)

    exit()



 