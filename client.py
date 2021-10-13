#!/usr/bin/python3

import asyncio
from input_handler import poll_stdin
from threading import Thread
from queue import Queue


class ChatClient(asyncio.BufferedProtocol):
    def __init__(self, on_connection_lost):
        self.on_connection_lost = on_connection_lost
        self.buf_sz = 64  # Default buffer size
        self.input_queue = Queue()

    def connection_made(self, transport):
        print("Connected to Server")
        # launch a seperate user-thread for handling standard input
        self.input_handler = Thread(
                target=poll_stdin,
                args=(self.input_queue, transport),
                daemon=True)
        self.input_handler.start()

    def get_buffer(self, size_hint):
        # Use either the default bufsize or use the recommended amount
        buffer_size = self.buf_sz if size_hint == -1 else size_hint
        buf = bytearray(buffer_size)
        self.data_view = memoryview(buf)
        return self.data_view

    def buffer_updated(self, nbytes):
        # Decode the received raw bytes and print to console
        print(f"S:{bytes(self.data_view[:]).decode()}")

    def connection_lost(self, exc):
        # Emit connection_lost signal
        self.on_connection_lost.set_result(True)
        print("Disconnected from server")


async def main():
    # use the main loop
    loop = asyncio.get_running_loop()
    # construct connection_lost future
    on_connection_lost = loop.create_future()

    # Connects to server using ChatClient protocol
    connection = await loop.create_connection(
            lambda: ChatClient(on_connection_lost),
            '127.0.0.1', 8083)

    transport = connection[0]

    # close the connection transport once connection lost signal is emitted
    await on_connection_lost
    transport.close()


asyncio.run(main())
