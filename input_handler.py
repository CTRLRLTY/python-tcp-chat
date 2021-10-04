def poll_stdin(input_queue, transport):
    """ wait for standard input """
    while True:
        if not input_queue.empty():
            send_data = input_queue.get()
            # send data to peer
            transport.write(send_data.encode())

        input_data = input()
        input_queue.put(input_data)
