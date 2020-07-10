# Thomas Brijs 2020
# Websocket client with HTTP Auth for Face recognition cameras
#!/usr/bin/python3 -u
import websocket
import time
import base64
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(5)
            ws.send(u'value')
        time.sleep(10)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    user = 'root'
    passwd = 'pass'
    auth = f'{user}:{passwd}'
    basicAuth = base64.b64encode(auth.encode()).decode()
    auth_header = f'Authorization: Basic {basicAuth}'
    ws_proto_header = 'Sec-Websocket-Protocol: tracker-protocol'
    ws_ext_header = 'Sec-Websocket-Extensions: permessage-deflate; client_max_window_bits'
    ws = websocket.WebSocketApp(f"ws://hostname/ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,
                              header = [auth_header, ws_ext_header, ws_proto_header])
    ws.on_open = on_open
    ws.run_forever()

