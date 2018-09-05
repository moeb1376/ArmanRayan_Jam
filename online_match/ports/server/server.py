import threading

import online_match.ports.server.logic_manager as logic_manager
import online_match.ports.server.io_manager as io_manager
import online_match.ports.server.graphic_manager as graphic_manager
import online_match.ports.server.CONST as CONST
import os
import requests


class GameManager:
    def __init__(self, condition_variable):
        self.graphic_manager = graphic_manager.GraphicManager()
        self.io_manager = io_manager.IOManager(self.graphic_manager, condition_variable)
        self.logic_manager = logic_manager.LogicManager()
        self.game_finish = -1
        self.log_file = open('online_match/ports/server/test.AbaloneLog', 'w')

    def start(self,win):
        self.io_manager.init_IO()
        self.log_file.write(
            self.io_manager.input_manager[0].name + '|' + self.io_manager.input_manager[1].name + '\n')
        output = self.logic_manager.build_output(ID=0)
        print("First output:", output)
        self.io_manager.set_output(output)
        # self.io_manager.set_game_start()
        while self.game_finish == -1:
            try:
                flag = True
                index = int(self.logic_manager.round // 0.5) % 2
                while flag and self.io_manager.input_manager[index].spend_time < CONST.ServerSocket.MAX_TIME_RECV:
                    input = self.io_manager.get_input()
                    print("input:", input)
                    output = self.logic_manager.play(input)
                    print("output : ", output)
                    if output.get("Last_Change", {}).get("ID", -2) == 1 or \
                                    output.get("Last_Change", {}).get("ID", -2) == 2:
                        self.logic_manager.round += 0.5
                        self.io_manager.change_input_turn()
                        self.log_file.write(self.creat_log_line(
                            output.get("Last_Change", {})) + '\n')
                        flag = False
                    else:
                        self.io_manager.set_output(output, index)
                    print("Spend Time : ", self.io_manager.input_manager[0].number,
                          self.io_manager.input_manager[0].spend_time,
                          self.io_manager.input_manager[1].number,
                          self.io_manager.input_manager[1].spend_time,
                          self.logic_manager.round)
                self.game_finish = self.logic_manager.check_game_finish()
                # self.graphic_manager.draw_points(self.logic_manager.player_points)
                if self.game_finish == -1:
                    if round(self.io_manager.input_manager[1].spend_time, 3) >= CONST.ServerSocket.MAX_TIME_RECV:
                        self.game_finish = 1
                    if round(self.io_manager.input_manager[0].spend_time, 3) >= CONST.ServerSocket.MAX_TIME_RECV:
                        self.game_finish = 2
                if self.game_finish == -1:
                    if self.logic_manager.round < CONST.Game.MAX_ROUND:
                        self.io_manager.set_output(output)
            except Exception as e:
                print("Game Error")
                raise
        msg = 'Player %d (%s) is Win'
        if self.game_finish == 0:
            print("Draw")
            self.log_file.write('Draw' + '\n')
        elif self.game_finish == 1:
            print(msg % (1, self.io_manager.input_manager[0].name))
            self.log_file.write(
                msg % (1, self.io_manager.input_manager[0].name) + '\n')

        elif self.game_finish == 2:
            print(msg % (2, self.io_manager.input_manager[1].name))
            self.log_file.write(
                msg % (2, self.io_manager.input_manager[1].name) + '\n')
        self.io_manager.set_output({"ID": 5})
        win[0] = self.game_finish
        return self.game_finish
        # self.log_file.close()

    def creat_log_line(self, last_change):
        result = []
        keys = sorted(last_change.keys())
        keys.remove('ID')
        for i in keys:
            result.append(last_change[i])
        return '|'.join(result)


if __name__ == "__main__":
    print('WTF', os.getcwd())
    cv = threading.Condition()
    game_manager = GameManager(cv)
    game_manager.start()
    # input("press any key to continue")
    url = "http://127.0.0.1:8000/online_match_result"

    payload = "{\"team1\":12,\"team2\":10,\"log_address\":\"/home/moeb/AppData/\",\"winner\":1}"
    headers = {
        'Accept': "application/json",
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': "90eb631e-deaf-4397-a0ac-0e52fbbb30b7"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
