import CONST


class LogicManager:
    def __init__(self):
        self.player_points = [0, 0]
        self.board = AbaloneBoard()
        self.player_marbles = self.board.get_player_marbles()
        print('player marbles : ', self.player_marbles[0], '\t', self.player_marbles[1])
        self.round = 0.0
        self.turn = 1
        self.marbles_out = [0, 0]

    def play(self, client_input):
        # self.round += 0.5
        if client_input == CONST.IOMsg.SERVER_INPUT_MSG:
            print("MSG is empty")
            return self.build_output(ID=-1)
        marbles = CONST.convert_coordinate(client_input["Marbles"])
        move = CONST.convert_coordinate(client_input["Head_To"])[0]
        head = CONST.convert_coordinate(client_input["Head"])[0]
        player_id = client_input["ID"]
        if head not in marbles:
            print("head not in marbels", type(head), head, marbles)
            return self.build_output(ID=4)
        if player_id != self.turn:
            print("ID player", player_id, "is not correct", self.turn)
            return self.build_output(ID=3)
        len_marbles = len(marbles)
        if len_marbles == 1:
            if not (self.board.check_point(move) and self.board.check_point(marbles[0])):
                return self.build_output(ID=4)
            if not self.check_empty_cell([move]) or self.check_empty_cell([marbles[0]]):
                print("Selected cell is not empty")
                return self.build_output(ID=4)
            if move not in self.board.get_neighbours(marbles[0]):
                print("Selected cell is not neighbours")
                return self.build_output(ID=4)
            if marbles[0] not in self.player_marbles[player_id - 1]:
                print("Selected marble is not correct")
                return self.build_output(ID=4)
            self.board.set_data(move, self.board.get_data(marbles[0]))
            self.board.set_data(marbles[0], 0)
            self.player_marbles[player_id - 1].append(move)
            del self.player_marbles[player_id - 1][self.player_marbles[player_id - 1].index(marbles[0])]
            return self.build_output(client_input, ID=self.turn)
        elif len_marbles == 2:
            marble1 = marbles[0]
            marble2 = marbles[1]
            if not (self.board.check_point(move) and self.board.check_point(marble1)
                    and self.board.check_point(marble2)):
                return self.build_output(ID=4)
            if marble2 not in self.board.get_neighbours(marble1):
                print("marbles isn't in neighbourhood ")
                return self.build_output(ID=4)
            if move not in self.board.get_neighbours(head):
                print("Selected cell is not neighbours")
                return self.build_output(ID=4)
            if not (marble1 in self.player_marbles[player_id - 1] and marble2 in self.player_marbles[player_id - 1]):
                print("Selected marble is not correct")
                return self.build_output(ID=4)
            type_of_move = self.type_of_move(marbles, head, move)
            if type_of_move == 'broadside':
                if self.check_empty_cell(marbles, x=move[0] - head[0], y=move[1] - head[1]):
                    self.set_move(marbles, head, move, player_id)
                    return self.build_output(client_input, ID=self.turn)
                else:
                    print("cell is not empty")
                    return self.build_output(ID=4)
            elif type_of_move == 'incorrect':
                print("move incorrect")
                return self.build_output(ID=4)
            else:
                t = self.get_enemy_number(marbles, player_id, x=move[0] - head[0], y=move[1] - head[1])
                if t > 1:
                    print("can't push enemy")
                    return self.build_output(ID=4)
                elif t == -1:
                    print("marbles among teammate")
                    return self.build_output(ID=4)
                else:
                    print('before set push2 ', self.player_marbles)
                    temp = self.player_marbles.copy()
                    self.set_push(marbles, player_id, t, x=move[0] - head[0], y=move[1] - head[1])
                    print('after set push2 ', self.player_marbles)
                    for i in temp[0]:
                        if i not in self.player_marbles[0]:
                            print(i)
                    for i in temp[1]:
                        if i not in self.player_marbles[1]:
                            print(i)
                    return self.build_output(client_input, ID=self.turn)
        if len(marbles) == 3:
            if not (all([self.board.check_point(i) for i in marbles]) and self.board.check_point(move)):
                return self.build_output(ID=4)
            if move not in self.board.get_neighbours(head):
                print("Selected cell is not neighbours")
                return self.build_output(ID=4)
            if not (all([i in self.player_marbles[player_id - 1] for i in marbles])):
                print(self.player_marbles[player_id - 1], '****', marbles)
                print("Selected marble is not correct")
                return self.build_output(ID=4)
            if not self.check_in_line(marbles):
                print("selected marbles not in line ")
                return self.build_output(ID=4)
            type_of_move = self.type_of_move(marbles, head, move)
            if type_of_move == 'broadside':
                if self.check_empty_cell(marbles, x=move[0] - head[0], y=move[1] - head[1]):
                    self.set_move(marbles, head, move, player_id)
                    return self.build_output(client_input, ID=self.turn)
                else:
                    print("cell is not empty")
                    return self.build_output(ID=4)
            elif type_of_move == 'incorrect':
                print("move incorrect")
                return self.build_output(ID=4)
            else:
                t = self.get_enemy_number(marbles, player_id, x=move[0] - head[0], y=move[1] - head[1])
                if t > 2:
                    print("can't push enemy")
                    return self.build_output(ID=4)
                elif t == -1:
                    print("marbles among teammate")
                    return self.build_output(ID=4)
                else:
                    print('before set push3 ', self.player_marbles)
                    temp = self.player_marbles.copy()
                    self.set_push(marbles, player_id, t, x=move[0] - head[0], y=move[1] - head[1])
                    print('after set push3 ', self.player_marbles)
                    for i in temp[0]:
                        if i not in self.player_marbles[0]:
                            print(i)
                    for i in temp[1]:
                        if i not in self.player_marbles[1]:
                            print(i)
                    return self.build_output(client_input, ID=self.turn)

    def build_output(self, last_change=CONST.IOMsg.SERVER_OUTPUT_MSG, **kwargs):
        print('build output : ', last_change, kwargs)
        if kwargs.get('ID') == 2 or kwargs.get('ID') == 1:
            self.turn = (self.turn % 2) + 1
            result = {}
            for i in last_change:
                if i == 'ID':
                    # temp = self.round / 0.5 % 2
                    # print("Temp : ",temp,self.round)
                    # result[i] = 1 if int(temp) == 1 else 2
                    result[i] = kwargs.get("ID", -2)
                elif i != 'Password':
                    result[i] = last_change.get(i, '')
            return {"Last_Change": result, "Board": self.board.board}
        else:
            return {"Last_Change": {"ID": kwargs.get('ID')}, "Board": self.board.board}

    def check_empty_cell(self, points, **kwargs):
        x = kwargs.get('x', 0)
        y = kwargs.get('y', 0)
        for i, j in points:
            if self.board.get_data((i + x, j + y)) != 0:
                return 0
        return 1

    def type_of_move(self, marbles, head, move):
        x = move[0] - head[0]
        y = move[1] - head[1]
        result = []
        for i in marbles:
            result.append((i[0] + x, i[1] + y))
        for i in result:
            if i in marbles:
                return "in-line"
            if not self.board.check_point(i):
                return 'incorrect'
        return 'broadside'

    def set_move(self, marbles, head, move, player_id):
        x = move[0] - head[0]
        y = move[1] - head[1]
        for i in marbles:
            new_move = (i[0] + x, i[1] + y)
            self.board.set_data(new_move, self.board.get_data(i))
            self.board.set_data(i, 0)
            self.player_marbles[player_id - 1].append(new_move)
            del self.player_marbles[player_id - 1][self.player_marbles[player_id - 1].index(i)]

    def get_enemy_number(self, marbles, player_id, **kwargs):
        x = kwargs.get('x')
        y = kwargs.get('y')
        target = [-1, -1]
        result = 0
        for i, j in marbles:
            data = self.board.get_data((i + x, j + y))
            if data == (player_id) % 2 + 1:
                target = [i + x, j + y]
                break
            elif data == 0:
                return 0
        if target == [-1, -1]:
            return -1
        while 0 <= target[0] <= 8 and 0 <= target[1] <= 8:
            data = self.board.get_data(target)
            if data == player_id:
                result == -1
                break
            if data <= 0:
                break
            result += 1
            target[0] += x
            target[1] += y
        return result

    def set_push(self, marbles, player_id, t, x,y):
        # t = number of enemy // x = move[0] - head[0] // y = move[1] - head[1]
        print()
        print("set push is running")
        print()
        i = marbles[0]
        print('marbels , i ,x ,y ,t', self.player_marbles[player_id - 1], i, x, y, t)
        while tuple(i) in marbles:  # peyda kardan aghab tarin marble
            i = [i[0] - x, i[1] - y]
        i = [i[0] + x, i[1] + y]
        print("target : ", i, t)
        j = len(marbles) + t
        back = player_id
        del self.player_marbles[player_id - 1][self.player_marbles[player_id - 1].index(tuple(i))]
        print("player id Del (%d,%d) in player %d" % (i[0], i[1], player_id))
        self.board.set_data(i, 0)
        while j > 0:
            next_cell = (i[0] + x, i[1] + y)
            if not self.board.check_point(next_cell):
                break
            temp = self.board.get_data(next_cell)

            print(next_cell, "->", back, temp)
            self.board.set_data(next_cell, back)

            if back == 0:
                pass
            elif temp == 0:
                print("append into player %d add (%d,%d)" % (back - 1, next_cell[0], next_cell[1]))
                self.player_marbles[back - 1].append(next_cell)
            elif temp != back:
                del self.player_marbles[temp - 1][self.player_marbles[temp - 1].index(next_cell)]
                print("temp Del (%d,%d) in player %d" % (next_cell[0], next_cell[1], temp))
                self.player_marbles[back - 1].append(next_cell)
                # self.board.set_data(i, back)
            back = temp
            j -= 1
            i = list(next_cell)

    @staticmethod
    def check_in_line(marbles):
        if (sum([marbles[i][0] == marbles[i + 1][0] for i in range(len(marbles) - 1)])) == len(marbles) - 1:
            return True
        elif (sum([marbles[i][1] == marbles[i + 1][1] for i in range(len(marbles) - 1)])) == len(marbles) - 1:
            return True
        elif sorted(marbles, key=lambda x: x[0]) == sorted(marbles, key=lambda x: x[1]):
            return True
        return False
        # print(tmp)
        # x1 = marbles[0][0] - marbles[1][0]
        # y1 = marbles[0][1] - marbles[1][1]
        # print("Check In Line : ", marbles, '\n', [(i[0] + x1, i[1] + y1) for i in marbles], '\n',
        #       [(i[0] - x1, i[1] - y1) for i in marbles])
        # temp = [(i[0] + x1, i[1] + y1) in marbles for i in marbles]
        # temp.extend([(i[0] - x1, i[1] - y1) in marbles for i in marbles])
        # if sum(temp) != 4:
        #     print("in line : ** sum(temp) != 4 ", temp)
        #     return False
        # counter = 0
        # for i in range(len(tmp)):
        #     for j in range(i + 1, len(tmp)):
        #         if tmp[i] == tmp[j]:
        #             counter += 1
        # print(tmp, counter)
        # return counter >= 2

    def check_game_finish(self):
        self.calculate_points()
        print("Marble out : ", len(self.player_marbles[0]), len(self.player_marbles[1]))
        print("Marble out : ", self.marbles_out)
        if self.round < CONST.Game.MAX_ROUND:
            if len(self.player_marbles[0]) <= CONST.Game.MARBLE_WIN:
                return 2
            if len(self.player_marbles[1]) <= CONST.Game.MARBLE_WIN:
                return 1
            return -1
        else:
            if len(self.player_marbles[0]) <= CONST.Game.MARBLE_WIN:
                return 2
            if len(self.player_marbles[1]) <= CONST.Game.MARBLE_WIN:
                return 1
            if len(self.player_marbles[0]) > len(self.player_marbles[1]):
                return 1
            elif len(self.player_marbles[0]) < len(self.player_marbles[1]):
                return 2
            else:
                if self.player_points[0] > self.player_points[1]:
                    return 1
                elif self.player_points[0] < self.player_points[1]:
                    return 2
                else:
                    return 0

    def calculate_points(self):
        self.player_points = [0, 0]
        for i in range(len(self.player_marbles)):
            distance_point = 0
            connectivity_point = 0
            for j in self.player_marbles[i]:
                distance_point += abs(self.get_distance_to_center(j))
                neighbours = self.board.get_neighbours(j)
                for k in neighbours:
                    if self.board.get_data(k) == i + 1:
                        connectivity_point += 1
                    elif self.board.get_data(k) == (i + 1) % 2 + 1:
                        connectivity_point -= 1
            self.player_points[i] = connectivity_point + distance_point

    @staticmethod
    def get_distance_to_center(point):
        x, y = point
        tmp = [x - 4, y - 4]
        if x == 4:
            return abs(y - 4)
        if y == 4:
            return abs(x - 4)
        if (x > 4 and y > 4) or (x < 4 and y < 4):
            return max(tmp, key=lambda i: abs(i))
        return abs(tmp[0]) + abs(tmp[1])


class AbaloneBoard:
    def __init__(self):
        self.player_marbles = [[], []]
        self.board = self.create_board()
        self.init_start_game()
        print('\n'.join([' '.join([str(j) for j in i]) for i in self.board]))

    def __str__(self):
        result = ''
        for i in self.board:
            result += str(i) + "\n"
        return result

    @staticmethod
    def create_board():
        result = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(4):
            for j in range(5 + i, 9):
                result[i][j] = -1
                result[j][i] = -1
        print('len result ', len(result), [len(i) for i in result])
        return result

    def init_start_game(self):
        # self.board[0][0:5] = [1 for _ in range(5)]
        # self.board[1][0:6] = [1 for _ in range(6)]
        # self.board[2][2:5] = [1 for _ in range(3)]
        # self.board[-1][4:9] = [2 for _ in range(5)]
        # self.board[-2][3:9] = [2 for _ in range(6)]
        # self.board[-3][4:7] = [2 for _ in range(3)]
        for i in range(5):
            self.board[i][0] = 1
            self.player_marbles[0].append((i, 0))
            self.board[8 - i][-1] = 2
            self.player_marbles[1].append((8 - i, 8))
        for i in range(6):
            self.board[i][1] = 1
            self.player_marbles[0].append((i, 1))
            self.board[8 - i][-2] = 2
            self.player_marbles[1].append((8 - i, 7))
        for i in range(2, 5):
            self.board[i][2] = 1
            self.player_marbles[0].append((i, 2))
            self.board[8 - i][-3] = 2
            self.player_marbles[1].append((8 - i, 6))

    def check_point(self, point, log=True):
        x, y = point
        if not (0 <= x < 9 and 0 <= y < 9):
            if log:
                print("point is not correct")
            return False
        elif self.board[x][y] == -1:
            if log:
                print("point is not correct")
            return False
        else:
            return True

    def get_neighbours(self, point):
        result = [(point[0], point[1] + 1), (point[0], point[1] - 1),
                  (point[0] + 1, point[1] + 1), (point[0] - 1, point[1] - 1),
                  (point[0] - 1, point[1]), (point[0] + 1, point[1])]

        i = 0
        while i < len(result):
            if self.check_point(result[i], False):
                i += 1
            else:
                del result[i]
        return result

    def get_data(self, point):
        if self.check_point(point):
            return self.board[point[0]][point[1]]
        else:
            return -2

    def set_data(self, point, value):
        if self.check_point(point):
            self.board[point[0]][point[1]] = value
        else:
            print("Set_Value : Point is not correct")

    def get_player_marbles(self):
        return self.player_marbles
