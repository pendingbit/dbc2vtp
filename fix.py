fix_header = '''
/* ************************************************************************** */
/*                                                                            */
/*                    Mentor Graphics Corporation                             */
/*                        All rights reserved                                 */
/*                           NBYX Created                                     */
/* ************************************************************************** */
/*                                                                            */
/*  Description:   Fix file for Volcano 7.2                                  */
/*                                                                            */
/* ************************************************************************** */
/*                                                                            */
/*                                                                            */
/* ************************************************************************** */
/* Auto generated by dbcConvertTool.py                                        */
/*                                                                            */
/* ************************************************************************** */


fixed_file;
volcano version "7.2";

volcano processing period 5 ms; 

network interface SCU_CAN_IF {
	Baud rate 500 kHz;

	supports mode FM_NORMAL;
	supports mode FM_QUIET;
	supports mode FM_SILENT;
	transmit interrupt true;
	receive interrupt true;
} 

'''



def CreateFix(dbclist, node):
    fixfile = open("target.fix","w+")
    fixfile.writelines(fix_header)

    #处理接收信号量
    fixfile.writelines("/*    Subscribed Signals    */\n")
    for i in range(len(dbclist)):
        if 'transmitter' in dbclist[i]:
            if dbclist[i]['transmitter'] != node:
                j = i+1
                while (j < len(dbclist)) and ('transmitter' not in dbclist[j]):
                    fixfile.writelines('signal '+dbclist[j]['signal_name']+'{\n')
                    fixfile.writelines('    subscribed;\n')
                    size = int(dbclist[j]['signal_size'])
                    if size == 1:
                        fixfile.writelines('    type boolean;\n')
                        fixfile.writelines('    size 1;\n')
                    elif size <= 32:
                        fixfile.writelines('    type unsigned;\n')
                        fixfile.writelines('    size '+dbclist[j]['signal_size']+';\n')
                    elif size%8 == 0:
                        fixfile.writelines('    type byte;\n')
                        fixfile.writelines('    size '+str(round(size/8))+';\n')
                    else:
                        print("THE SIGNAL SIZE IS ERROR, PLEASE CHECK IT!!!")
                        
                    fixfile.writelines('}\n\n')
                    j += 1

    #处理发送信号量
    fixfile.writelines("/*    Published Signals    */\n")
    for i in range(len(dbclist)):
        if 'transmitter' in dbclist[i]:
            if dbclist[i]['transmitter'] == node:
                j = i+1
                while (j < len(dbclist)) and ('transmitter' not in dbclist[j]):
                    fixfile.writelines('signal '+dbclist[j]['signal_name']+'{\n')
                    fixfile.writelines('    published;\n')
                    size = int(dbclist[j]['signal_size'])
                    if size == 1:
                        fixfile.writelines('    type boolean;\n')
                        fixfile.writelines('    size 1;\n')
                    elif size <= 32:
                        fixfile.writelines('    type unsigned;\n')
                        fixfile.writelines('    size '+dbclist[j]['signal_size']+';\n')
                    elif size%8 == 0:
                        fixfile.writelines('    type byte;\n')
                        fixfile.writelines('    size '+str(round(size/8))+';\n')
                    else:
                        print("THE SIGNAL SIZE IS ERROR, PLEASE CHECK IT!!!")
                        
                    fixfile.writelines('}\n\n')
                    j += 1
                    
    #处理立即帧
    fixfile.writelines("/*    Immediate Signal Groups    */\n")
    for i in range(len(dbclist)):
        if ('SendType' in dbclist[i]) and (dbclist[i]['SendType'] == '5'):#5代表立即帧
            fixfile.writelines('immediate frame '+dbclist[i]['message_name']+' {\n')
            if dbclist[i]['transmitter'] == node:
                fixfile.writelines('    transmitted;\n')
            else:
                fixfile.writelines('    received;\n')
            j = i+1
            while (j < len(dbclist)) and ('transmitter' not in dbclist[j]):
                fixfile.writelines('    contains signal '+dbclist[j]['signal_name']+';\n')
                j += 1
            fixfile.writelines('}\n')


    fixfile.flush()
    fixfile.close()

    return 