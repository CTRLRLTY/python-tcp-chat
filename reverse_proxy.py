#!/usr/bin/python3

import asyncio


async def relay_handler(reader, writer):
    while True:
        raw_data = await reader.read(64)
        data = raw_data.decode()
        if data.isdigit():
            writer.write(raw_data)
            await writer.drain()
            print(f"FOWARDED: {data}")
        else:
            print(f"REJECTED: {data}")


async def proxy_cb(sr, sw, cr, cw):
    server_handler = asyncio.create_task(relay_handler(sr, cw))
    client_handler = asyncio.create_task(relay_handler(cr, sw))
    await asyncio.wait([server_handler, client_handler])


async def main():
    client_reader, client_writer = await asyncio.open_connection(
            '127.0.0.1', 6969)
    print("Connected to server")
    proxy_server = await asyncio.start_server(
            lambda r, w: proxy_cb(r, w, client_reader, client_writer),
            '127.0.0.1', 8083)
    print("Proxy Started")

    async with proxy_server:
        await proxy_server.serve_forever()

asyncio.run(main())
