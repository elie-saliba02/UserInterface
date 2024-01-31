# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
from bleak import BleakClient, BleakScanner
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import os


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


SSMACHMO = "C4EBA289-0112-4CDD-9060-996097BBFA23"

def binary_to_decimal(line):
    if int(line, 16) & 0b00000000000000001000000000000000:
        line = - (int(line, 16) & 0b00000000000000000111111111111111)
        line = line / 32767
        #print(line)
    else:
        line = int(line, 16) & 0b00000000000000000111111111111111
        line = line / 32767
        #print(line)
    return line


class GATT_Client(BleakClient):
    def __init__(self):
        self.client_uuid = SSMACHMO  # "2427B6C6-49DE-45AF-A0EE-2F2997CA33F4"
        super().__init__(self.client_uuid)
        self.ind = 0
        self.list_ = []

    async def GATT_connect(self):
        try:
            print("Trying to Connect")
            await self.connect()
            print('Succesfully Connected to Device')
        except Exception as e:
            print(e)

    def notification_handler_2(self, sender, datas):
        """Simple notification handler which prints the data received."""
        #print("Notification Handler")
        #We will be receiving the data in an array of 244 elements. Each element is One Byte.
        #Write the data in an array, then write the array to a file.
        #Receive the data over notifications
        #Write the data to a file
        #Convert the data to decimal
        #for ... in ...
        #print(len(data))
        '''
        for data in datas:
            print(hex(data))
        '''
        '''
        for data in datas: #datas[::2]: #range(0, len(datas), 1):
            #self.ind += 1
            print(hex(data)[2:])
            #self.list_ += hex(data)


        print("BREAK")
        '''

        it = iter(datas)
        for x, y in zip(it, it):
            var = str(hex(x)[2:] + str(hex(y)[2:]) + '\n')
            #print(hex(x)[2:], hex(y)[2:])
            #print("FOR LOOP")
            #print(var)
            self.list_ += var
            #print(hex(y)[2:])


        #print(hex(data[0]), hex(data[1]), hex(data[2]), hex(data[3]), hex(data[4]), hex(data[5]), hex(data[6]), hex(data[7]), hex(data[8]), hex(data[9]), hex(data[10]), hex(data[11]), hex(data[12]), hex(data[13]), hex(data[14]), hex(data[15]), hex(data[16]), hex(data[17]), hex(data[18]), hex(data[19]), hex(data[20]), hex(data[21]), hex(data[22]), hex(data[23]), hex(data[24]), hex(data[25]), hex(data[26]), hex(data[27]))
        #print(hex(data[0]))
        #print(data[0], data[1])

        '''
        # print(data[0], data[1]])
        print(len(data))
        temp = ((data[0] * 256) + data[1]) / 1000
        print("Temp Is : ")
        print(temp)
        '''

#class Window(QWidget):


async def main():
    ind = 0
    print("discovering")
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

    client = GATT_Client()
    await client.GATT_connect()

    '''
    result = await client.read_gatt_char("180D")
    print(result)
    '''

    # print(client.services)

    for service in client.services:
        print(service)

        for char in service.characteristics:
            print("  ", char)


    '''
    await client.write_gatt_char("a91a350c-d937-44c1-a7a2-5f9a5aa68c3f", bytearray(b'\x01'))
    await asyncio.sleep(1)
    '''

    await client.start_notify(12, client.notification_handler_2)
    print("Receiving")
    await asyncio.sleep(1)
    print("Receiving 2")
    await client.stop_notify(12)
    print("done")
    with open('mic.txt', 'w') as d:
        d.writelines(client.list_)
    with open('mic.txt', 'r') as f:
        lines = f.readlines()
    # remove spaces
        #lines = [line.replace(' ', '') for line in lines]
        lines = [binary_to_decimal(line) for line in lines]
        lines = [str(line) + '\n' for line in lines]
    with open('mic2.txt', 'w') as d:
        d.writelines(lines)
    await asyncio.sleep(5)
    print(client.ind)
    print("Shutting Down")

asyncio.run(main())

#handle 10
#handle 11 need to be changed
#handle 12