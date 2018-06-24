import json
import random
import socket
import threading
import time
import CONST


class MySocket:
    def __init__(self, socket_number, socket_pass, socket_obj, socket_address):
        self.number = socket_number
        self.password = socket_pass
        self.socket_obj = socket_obj
        self.address = socket_address
        self.name = ''
        self.spend_time = 0
        self.game_is_done = False
        self.thread = threading.Thread(target=self.get_input)
        self.my_task = []

    def establish_connection(self):
        msg = {"ID": self.number, "Password": self.password}
        json_msg = json.dumps(msg)
        self.socket_obj.send(json_msg.encode("ascii"))
        json_recv = self.socket_obj.recv(CONST.ServerSocket.MAX_DATA_RECV_SIZE).decode('ascii')
        try:
            recvmsg = json.loads(json_recv)
        except:
            print(json_recv)
            print('player', self.number, "Client Input Data Not Jason")
            return False
        if recvmsg.keys() != CONST.EstablishConnection.CLIENT_MSG.keys():
            print('player', self.number, "Incorrect Massage", recvmsg)
            return False
        if recvmsg["Status"] != CONST.EstablishConnection.STATUS_ACCEPTED:
            print("player", self.number, "Could'nt Connect")
            return False
        self.name = recvmsg.get("Name", "NoName" + str(self.number))
        return True

    def get_input(self):
        while not self.game_is_done:
            json_recv = self.socket_obj.recv(CONST.ServerSocket.MAX_DATA_RECV_SIZE).decode('ascii')
            # print("json recv , number ",json_recv,self.number,time.time())
            try:
                recvmsg = json.loads(json_recv)
            except:
                recvmsg = CONST.IOMsg.SERVER_INPUT_MSG
            if recvmsg != CONST.IOMsg.SERVER_INPUT_MSG:
                self.validation_password(recvmsg)
            self.my_task.append(recvmsg)
            # print("add task")

    def validation_password(self, recmsg):
        if recmsg.get("Password", CONST.IOMsg.DEFAULT_PASSWORD) != self.password:
            raise Exception("player", self.name, self.number, "Password is not correct")

    def set_output(self, msg):
        if not (-2 < msg['ID'] < 6):
            print("Output Format is not correct")
            return False
        output_msg = json.dumps(msg).encode("ascii")
        self.socket_obj.send(output_msg)


class IOManager:
    def __init__(self, graphic_manager):
        self.graphic_manager = graphic_manager
        self.input_turn = 0
        self.input_manager = []
        self.output_manager = [self.graphic_manager]
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = CONST.ServerSocket.SERVER_HOST
        self.port = CONST.ServerSocket.SERVER_PORT

    def init_IO(self):
        self.build_server()
        self.build_client()

    def build_server(self):
        self.server_socket.settimeout(CONST.ServerSocket.TIME_OUT)
        print('Server Host & Port : ', self.host, self.port)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(CONST.ServerSocket.CLIENT_NUMBER)

    def build_client(self):
        self.graphic_manager.draw_menu()
        for i in range(CONST.ServerSocket.CLIENT_NUMBER):
            socket_obj, socket_address = self.server_socket.accept()
            client_socket = MySocket(i + 1, random.randrange(1000, 9999), socket_obj, socket_address)
            if client_socket.establish_connection():
                self.input_manager.append(client_socket)
                self.output_manager.append(client_socket)
                print('client', i + 1, 'with address', socket_address, " and name ", client_socket.name, 'added')
                self.graphic_manager.draw_menu_name(client_socket.name)
        self.server_socket.close()

    def get_input(self):
        input_manager = self.input_manager[self.input_turn]
        t = time.time()
        while round(time.time() - t, 3) <= CONST.ServerSocket.MAX_TIME_RECV and len(input_manager.my_task) == 0:
            continue
        print('Waiting time : ', round(time.time() - t, 3),time.time(),self.input_turn)
        input_manager.spend_time += round(time.time() - t, 3)
        if len(input_manager.my_task) > 0:
            temp = input_manager.my_task[0]
            del input_manager.my_task[0]
            return temp
        else:
            return CONST.IOMsg.SERVER_INPUT_MSG

    def change_input_turn(self):
        self.input_turn = (self.input_turn + 1) % len(self.input_manager)

    def set_output(self, output,index = -1):
        if index == -1:
            if output.get("ID",-2) == 5:
                for i in self.input_manager:
                    i.game_is_done = True
                    i.set_output({"ID":5})
            elif output.get("Last_Change",{}).get("ID",-2) == 0:
                self.output_manager[0].set_output(output['Board'])
                for i in self.input_manager:
                    i.set_output({"ID": 0})
                for i in self.input_manager:
                    i.thread.start()
            else:
                self.output_manager[0].set_output(output['Board'])
                self.output_manager[1].set_output(output['Last_Change'])
                self.output_manager[2].set_output(output['Last_Change'])
        else:
            self.output_manager[index+1].set_output(output['Last_Change'])

    def set_game_start(self):
        for i in self.input_manager:
            i.set_output({"ID": 0})
        for i in self.input_manager:
            i.thread.start()
