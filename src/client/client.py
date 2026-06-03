import socket, os, time
import pathlib

LOGGING = True
HOST = '127.0.0.1'
PORT = 50007

session = time.time()

file_path = pathlib.Path("logs")

log_buffer = []
def print_logger(string, logging = LOGGING):
    if logging:
        log_buffer.append(string)
    print(string)

def input_logger(logging=LOGGING):
    try:
        string = input()
    except EOFError:
        return 'QUIT'
    if logging:
        log_buffer.append(string)
    return string
    
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        f = s.makefile('rwb')
        while True:
            try: line = input_logger().strip()
            except: line = 'QUIT'
            if not line: continue
            if line.upper().startswith('FILE '):
                path = line.split(' ', 1)[1]
                try:
                    with open(path, 'rb') as fp: blob = fp.read()
                except: 
                    print_logger('unknown file location')
                    continue
                name = os.path.basename(path)
                header = f'FILE {name} {len(blob)}\n'.encode()
                f.write(header + blob)
                f.flush()
                reply = f.readline()
                if not reply:
                    break
                print_logger(reply.decode().strip())
                continue 
            else:
                f.write((line + '\n').encode())
                f.flush()
                reply = f.readline()
                if not reply:
                    break
                print_logger(reply.decode().strip())
            if line.upper().startswith('QUIT'):
                break
finally:
    with open(file_path / f"{session}", "w") as logfile:
        logfile.write('\n'.join(log_buffer))  