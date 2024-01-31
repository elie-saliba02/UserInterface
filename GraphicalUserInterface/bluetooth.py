import asyncio
from bleak import BleakScanner, BleakClient, BleakError
import queue
import threading
from asyncio import AbstractEventLoop
from typing import Callable, Optional
from concurrent.futures import Future


class BLE:
    def __init__(self, loop: AbstractEventLoop, callback: Callable[[list], None]):
        self.loop = loop
        self.callback = callback
        self.load_test_future: Optional[Future] = None
        self.scan(None)

    def scan(self, timeout):
        asyncio.run_coroutine_threadsafe(self._scan(timeout), self.loop)

    async def _scan(self, timeout):
        filtered_devices = []   #By Manufacturer (first 8 char of UUID)
        if not timeout:
            devices = await BleakScanner.discover()
        else:
            devices = await BleakScanner.discover(timeout=timeout)
        for device in devices:
            if str(device)[:8] == "C4EBA289" or str(device)[:8] == "153E524C":
                filtered_devices.append(device)
        self.callback(filtered_devices)

    def connect(self, address, callback_connected):
        asyncio.run_coroutine_threadsafe(self._connect(address), self.loop)
        self.callback_connected = callback_connected

    async def _connect(self, address):
        self.client = BleakClient(address)
        await self.client.connect()
        self.callback_connected()
        print("Connected")

    def blinkLed(self):
        asyncio.run_coroutine_threadsafe(self._blinkLed(), self.loop)

    async def _blinkLed(self):
        led = await self.client.read_gatt_char("5b026510-4088-c297-46d8-be6c736a087a")
        print(led)
        if led == bytearray(b'\x00'):
            await self.client.write_gatt_char("5b026510-4088-c297-46d8-be6c736a087a", bytearray(b'\x01'))
        else:
            await self.client.write_gatt_char("5b026510-4088-c297-46d8-be6c736a087a", bytearray(b'\x00'))

    def notify(self, notification_handler):
        asyncio.run_coroutine_threadsafe(self._notify(notification_handler), self.loop)

    async def _notify(self, notification_handler):
        await self.client.start_notify(29, notification_handler)
        await self.client.stop_notify(29)

    def sleep(self, duration):
        asyncio.run_coroutine_threadsafe(self._sleep(duration), self.loop)

    async def _sleep(self, duration):
        await asyncio.sleep(duration)


