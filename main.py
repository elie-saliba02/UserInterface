import asyncio
import sys
from queue import Queue
from concurrent.futures import Future
from asyncio import AbstractEventLoop
from typing import List, Dict, Set, Optional, Callable
from aiohttp import ClientSession
import aiohttp
from threading import Thread
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel
from bleak import BleakScanner, BleakClient
from PyQt5.QtCore import QTimer

#"153E524C-B6FF-49AF-AB0F-A96758E7AE1E" BLE
#"2427B6C6-49DE-45AF-A0EE-2F2997CA33F4" Blinky Example

class ScanTest:
    def __init__(self, loop: AbstractEventLoop, callback: Callable[[str], None]):
        self._loop = loop
        self._callback = callback
        self._load_test_future: Optional[Future] = None

    def start(self):
        future = asyncio.run_coroutine_threadsafe(self._scan(), self._loop)
        self._load_test_future = future

    def connect(self):
        asyncio.run_coroutine_threadsafe(self._connect(), self._loop)

    def update_char(self):
        asyncio.run_coroutine_threadsafe(self._update_char(), self._loop)

    async def _scan(self):
        devices = await BleakScanner.find_device_by_address("2427B6C6-49DE-45AF-A0EE-2F2997CA33F4")
        print(devices)
        self._callback(str(devices).strip("2427B6C6-49DE-45AF-A0EE-2F2997CA33F4:"))

    async def _connect(self):
        '''
        async with BleakClient("2427B6C6-49DE-45AF-A0EE-2F2997CA33F4") as client:
            print(client) When it exits this it disconnects
        '''
        self.client = BleakClient("2427B6C6-49DE-45AF-A0EE-2F2997CA33F4")
        await self.client.connect()
        print(self.client)


    async def _update_char(self):
        led = await self.client.read_gatt_char("5b026510-4088-c297-46d8-be6c736a087a")
        print(led)
        if led == bytearray(b'\x00'):
            await self.client.write_gatt_char("5b026510-4088-c297-46d8-be6c736a087a", bytearray(b'\x01'))
        else:
            await self.client.write_gatt_char("5b026510-4088-c297-46d8-be6c736a087a", bytearray(b'\x00'))
        '''
        print("Reading")
        print(self.client)
        led = await self.client.read_gatt_char("5b026510-4088-c297-46d8-be6c736a087a")
        print("Value Is")
        print(led)
        '''


class LoadScanner(QWidget):
    def __init__(self, loop):
        super().__init__()
        self._queue = Queue()
        self._loop = loop
        self._load_scan: Optional[ScanTest] = None
        self.setGeometry(100, 100, 250, 250)
        self.setWindowTitle('Example')
        self._scan = QPushButton('Scan', self)
        self._scan.clicked.connect(self._start)
        self._scan.move(10, 10)
        self.show()

    def _update_display(self, address: str):
        address_label = QLabel(self)
        address_label.setText(address)
        address_label.move(15, 43)
        address_label.show()
        self._connect = QPushButton('Connect', self)
        self._connect.clicked.connect(self._connected)
        self._connect.move(10, 60)
        self._connect.show()

    def _queue_update(self, address: str):
        self._queue.put(address)  # What do I want to put on the queue? The address of the device

    def _poll_queue(self):
        if not self._queue.empty():
            address = self._queue.get()
            self._update_display(address)
        else:
            if self._load_scan:
                QTimer.singleShot(1000, self._poll_queue)

    def _start(self):
        if self._load_scan is None:
            self.scan = ScanTest(self._loop, self._queue_update)
            QTimer.singleShot(1000, self._poll_queue)
            self.scan.start()
            self._load_scan = self.scan

    def _connected(self):
        print("Connecting")
        self.scan.connect()
        self._led = QPushButton('LED', self)
        self._led.clicked.connect(self._leded)
        self._led.move(10, 90)
        self._led.show()

    def _leded(self):
        self.scan.update_char()
        print("led")


class ThreadedEventLoop(Thread):
    def __init__(self, loop: AbstractEventLoop):
        super().__init__()
        self._loop = loop
        self.daemon = True

    def run(self):
        self._loop.run_forever()


loop = asyncio.new_event_loop()
#loop_2 = asyncio.new_event_loop()

asyncio_thread = ThreadedEventLoop(loop)
asyncio_thread.start()

#asyncio_thread_2 = ThreadedEventLoop(loop_2)
#asyncio_thread_2.start()

app = QApplication(sys.argv)
window = LoadScanner(loop)
#app_2 = QApplication(sys.argv)
#window_2 = LoadScanner(loop_2)
sys.exit(app.exec_())