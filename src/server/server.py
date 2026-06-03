import socket
import os
import time
import pathlib

file_path = pathlib.Path("logs") 


HOST = '127.0.0.1'
PORT = 50007
USERS_FILE = 'users.txt'
with open(USERS_FILE) as uf:
    USERS = {line.strip() for line in uf if line.strip()}

session = time.time()

log_buffer = []
def print_logger(string, logging = True):
    if logging:
        log_buffer.append(string)
    print(string)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            ip, port = addr
            print_logger(f"started connection at {ip} on port {port}")
            with conn:
                try:
                    f = conn.makefile('rwb')
                    user = None
                    while True:
                        line = f.readline()
                        if not line: break
                        parts = line.decode().strip().split(' ')
                        cmd = parts[0].upper()
                        arg = '' if len(parts) < 2 else " ".join(parts[1:])
                        if cmd =='LOGIN': 
                            if arg in USERS:
                                user = arg
                                print_logger(f'{user} has logged in')
                                f.write(b'OK\n')
                            else:
                                f.write(b'TRY AGAIN\n')
                                print_logger(f'{arg} tried to log in and failed')
                        elif cmd == 'MSG':
                            if not user or not arg:
                                f.write(b'TRY AGAIN\n')
                            else:
                                print_logger(f'{user}: {arg}')
                                f.write(b'OK\n')

                        elif cmd == 'FILE':
                            if len(parts) < 3:
                                f.write(b"TOO LITTLE ARGUMENTS\n")
                            else:
                                data = f.read(int(parts[-1]))
                                if not user:
                                    f.write(b'LOG IN FIRST\n')
                                elif len(parts) > 3:
                                    f.write(b"TOO MANY ARGUMENTS\n")
                                else:
                                    name = os.path.basename(parts[1])
                                    if name == 'users.txt':
                                        f.write(b"NO ACCESS FROM CLIENT\n")
                                    else:
                                        with open(os.path.join(".", name), 'wb') as wf:
                                            wf.write(data)
                                        f.write(b'FILE TRANSFER OK\n')
                                        print_logger(f"{user} saved {name}")
                            f.flush()

                            
                        
                        elif cmd == 'QUIT':
                            f.write(b'BYE\n')
                            print_logger(f"{user} has quit.")
                            f.flush()
                            break
                        else:
                            print_logger(line.decode().strip())
                            f.write(b'TRY AGAIN\n')

                        f.flush()
                    print_logger(f"terminated session with {ip} on port {port}")
                except:
                    print_logger('ERROR')
except:
    pass
finally:
    with open(file_path / f"{session}", "w") as logfile:
        logfile.write('\n'.join(log_buffer))            
        
