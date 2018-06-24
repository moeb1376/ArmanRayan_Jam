class ServerSocket:
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 5000
    CLIENT_NUMBER = CLIENT_SOCKET_NUMBER = 2
    TIME_OUT = 400
    MAX_DATA_RECV_SIZE = 2048
    MAX_DATA_SEND_SIZE = 2048
    MAX_TIME_RECV = 180


class EstablishConnection:
    DEFAULT_PASSWORD = 0
    STATUS_ACCEPTED = "DONE"
    SERVER_MSG = {"ID": "", "Password": DEFAULT_PASSWORD}
    CLIENT_MSG = {"Status": "", "Password": DEFAULT_PASSWORD, "Name": ""}


class IOMsg:
    DEFAULT_PASSWORD = 0
    # Marbles is a list of tuple
    # DEFAULT_MOVE = {"Marbles": [], "Option": {"Head": (), "Head_To": (), "Is_Inline_Move": True}}
    # DEFAULT_LAST_CHANGE = DEFAULT_MOVE
    # CLIENT_INPUT_MSG = {"Move": DEFAULT_MOVE, "Password": DEFAULT_PASSWORD, "ID": 0}
    # CLIENT_OUTPUT_MSG = {"Last_Change": DEFAULT_LAST_CHANGE, "Board": ""}
    SERVER_INPUT_MSG = {"Marbles": "", "Head": '', "Head_To": '', "Password": DEFAULT_PASSWORD, "ID": 0}
    SERVER_OUTPUT_MSG = {"Marbles": "", "Head": '', "Head_To": '', "ID": 0}
    # DONE_MSG = {"Done": True}
    # START_MSG = {"Start": True}
    MassageID = {-1: "MSG is empty",
                 0: "Start massage",
                 1: "Player 1 move",
                 2: "Player 2 move",
                 3: "ID incorrect",
                 4: "Wrong move",
                 5: "Done massage"}


class Game:
    MARBLE_WIN = 8
    MAX_ROUND = 150.0


def convert_coordinate(coordinate):
    if type(coordinate) == str:
        if len(coordinate) % 2 == 1:
            return "Not Correct"
        result = []
        for i in range(0, len(coordinate), 2):
            result.append((int(coordinate[i]), int(coordinate[i + 1])))
        return result
    elif type(coordinate) == list:
        result = ''
        for i in coordinate:
            for j in i:
                result += str(j)
        return result
    elif type(coordinate) == tuple:
        result = ''
        for i in coordinate:
            result += str(i)
        return result
    else:
        return ''
