"""
main paintbot class
"""


class PaintBot:
    """TODO add a doc string"""
    __pid = None
    __game = None
    __rotation = 0

    def __init__(self, game, pid):
        self.__game = game
        self.__pid = pid
        self.__rotation = 0

    # Access Game Information

    def get_x_size(self):
        return len(self.__game.board[0])

    def get_y_size(self):
        return len(self.__game.board)

    def get_turn(self):
        return int(self.__game.players[self.__pid]['turn'])

    def get_max_turns(self):
        return int(self.__game.max_turns)

    def is_playing(self):
        return self.get_turn() < self.__game.max_turns

    def get_number_of_players(self):
        return len(self.__game.players)

    def get_my_score(self):
        return int(self.__game.get_scores()[self.__pid])

    def get_player_score(self, pid):
        return int(self.__game.get_scores()[pid])

    def get_my_position(self):
        return list(self.__game.players[self.__pid]['position'])

    def get_player_position(self, pid):
        return list(self.__game.players[pid]['position'])

    def get_my_color(self):
        return int(self.__pid)

    def get_cell_color(self, x, y):
        board = self.__game.board
        if self.__game.is_in_bounds(x, y):
            cell = board[y][x]
            if cell is '.':
                return None
            return int(cell)
        return None

    def cell_is_occupied(self, x, y):
        pos = [x, y]
        if self.__game.is_in_bounds(x, y):
            for p in self.__game.players:
                if p['position'] == pos:
                    return True
        return False

    def cell_is_in_bounds(self, x, y):
        return self.__game.is_in_bounds(x, y)

    # Main Move Options

    def up(self):
        self.__rotation = 0
        self.__game.submit_move(self.__pid, 'up')

    def down(self):
        self.__rotation = 180
        self.__game.submit_move(self.__pid, 'down')

    def left(self):
        self.__rotation = 270
        self.__game.submit_move(self.__pid, 'left')

    def right(self):
        self.__rotation = 90
        self.__game.submit_move(self.__pid, 'right')

    def skip(self):
        self.__game.submit_move(self.__pid, 'skip')

    def face(self, direction):
        if direction == 'up':
            self.__rotation = 0
        elif direction == 'right':
            self.__rotation = 90
        elif direction == 'down':
            self.__rotation = 180
        elif direction == 'left':
            self.__rotation = 270

    def is_blocked(self):
        ahead = self.get_my_position()
        angle = self.__rotation
        if angle == 0:
            ahead[1] = ahead[1] - 1
        elif angle == 90:
            ahead[0] = ahead[0] + 1
        elif angle == 180:
            ahead[1] = ahead[1] + 1
        else:
            ahead[0] = ahead[0] - 1
        out_of_bounds = not self.cell_is_in_bounds(ahead[0], ahead[1])
        occupied = self.cell_is_occupied(ahead[0], ahead[1])
        return out_of_bounds or occupied

    # Experimental Methods

    def clockwise(self):
        new_rotation = (self.__rotation + 90) % 360
        self.__rotation = new_rotation

    def counterclockwise(self):
        new_rotation = self.__rotation - 90
        if new_rotation < 0:
            new_rotation = new_rotation + 360
        self.__rotation = new_rotation

    def forward(self):
        angle = self.__rotation
        if angle == 0:
            self.up()
        elif angle == 90:
            self.right()
        elif angle == 180:
            self.down()
        else:
            self.left()

    def backward(self):
        angle = self.__rotation
        if angle == 0:
            self.down()
        elif angle == 90:
            self.left()
        elif angle == 180:
            self.up()
        else:
            self.right()

    def is_at_edge(self, edge):
        board = self.__game.board
        pos = self.get_my_position()
        if edge is 'top':
            return pos[1] == 0
        if edge is 'bottom':
            return pos[1] == len(board)
        if edge is 'left':
            return pos[0] == 0
        if edge is 'right':
            return pos[0] == len(board[0])
        return False
