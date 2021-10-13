#!/usr/bin/python3

import asyncio
from input_handler import poll_stdin
from threading import Thread
from queue import Queue


class ChatServer(asyncio.BufferedProtocol):
    def __init__(self):
        self.buf_sz = 64  # Default buffer size
        self.input_queue = Queue()

    def connection_made(self, transport):
        print("Client Connected")
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
        print(f"P:{bytes(self.data_view[:]).decode()}")


async def main():
    # use the main loop
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: ChatServer(),
        'localhost', 6969
    )

    # tell the server to run forever...
    async with server:
        await server.serve_forever()

asyncio.run(main())
