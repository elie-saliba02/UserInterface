import sys
import gui
from PyQt5.QtWidgets import QApplication
import bluetooth as ble
import database as db
from bleak import BleakScanner
import asyncio
from threading import Thread
from asyncio import AbstractEventLoop
from typing import Callable, Optional
from concurrent.futures import Future
from queue import Queue

app = QApplication(sys.argv)

queue = Queue()


class Start:
    def __init__(self, ble_handle, db_handle):
        self.ble_handle = ble_handle
        self.db_handle = db_handle

    def run(self):
        print("run")
        gui.MainWindow(queue, self.ble_handle, app, self.db_handle)
        sys.exit(app.exec_())


class ThreadedEventLoop(Thread):
    def __init__(self, loop: AbstractEventLoop):
        super().__init__()
        self.loop = loop
        self.daemon = True

    def run(self):
        self.loop.run_forever()


ble_loop = asyncio.new_event_loop()

asyncio_bluetooth_thread = ThreadedEventLoop(ble_loop)
asyncio_bluetooth_thread.start()

''' Potential Database
db_loop = asyncio.new_event_loop()
asyncio_database_thread = ThreadedEventLoop(db_loop)
asyncio_database_thread.start()
'''


def queue_update(address: list):
    for add in address:
        queue.put(add)


device_list = []

bluetooth = ble.BLE(ble_loop, queue_update)

# database = db.DB(db_loop) #Potential Database

if __name__ == '__main__':
    Start(bluetooth, device_list).run()
