#coding=utf-8

InputDBC = input("Please Enter DBC file:")

temp = InputDBC.find('.dbc')
while(temp == -1):
    print("Invalid dbc file! Please input again!\r\n")
    InputDBC = input("Please Enter DBC file:")
    temp = InputDBC.find('.dbc')
print("The input DBC file is:", InputDBC)

dbc_fd = open(InputDBC, "r")

line = dbc_fd.readline()
while(line):
    print(line)
    line = dbc_fd.readline()

exit(0)