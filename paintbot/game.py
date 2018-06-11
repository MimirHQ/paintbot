"""
Main Game Client Class
"""


from paintbot.bot import (
    PaintBot
)
from threading import (
    Thread,
    Event
)
from time import (
    time
)


class PaintGame:
    """TODO need a docstring here"""
    board = None
    players = []
    move_flag = Event()
    max_turns = None
    bot_timelimit = None
    record = ''

    def __init__(self, x_size, y_size, max_turns=100, bot_timelimit=1):
        if x_size < 1:
            raise Exception('Board x size must be greater than 0.')
        if y_size < 1:
            raise Exception('Board y size must be greater than 0.')
        if max_turns < 1:
            raise Exception('Game turn limit must be greater than 0.')
        board = []
        for y in range(y_size):
            row = []
            for x in range(x_size):
                row.append('.')
            board.append(row)
        self.board = board
        self.max_turns = max_turns
        self.bot_timelimit = bot_timelimit
        self.record = str(x_size) + ',' + str(y_size)

    def add_player(self, main_fn, pos=[0, 0]):
        game = self
        pid = len(self.players)
        bot = PaintBot(game, pid)
        thread = Thread(name=('Player %d' % pid), target=main_fn, args=(bot,), daemon=True)
        self.players.append({
            'pid': pid,
            'bot': bot,
            'thread': thread,
            'is_playing': True,
            'position': pos,
            'turn': 0,
            'move': None,
            'did_move': False,
            'move_failed': False
        })
        if not self.is_in_bounds(pos[0], pos[1]):
            raise Exception('Tried to add player out of bounds.')
        cell = self.board[pos[1]][pos[0]]
        if cell is not '.':
            raise Exception('Tried to add player at occupied cell.')
        self.board[pos[1]][pos[0]] = str(pid)
        return pid

    def start(self):
        # Initialize game and player threads
        self.move_flag.clear()
        self.update_record([p['position'] for p in self.players])
        for player in self.players:
            thread = player['thread']
            thread.start()
        # Manage main game loop
        time_start = time()
        while True:
            # Check if all alive threads have made their moves
            moved_count = sum(1 if p['did_move'] else 0 for p in self.players)
            alive_count = sum(1 if self.bot_is_alive(p) else 0 for p in self.players)
            all_moved = moved_count == alive_count
            # print(moved_count, 'moved vs', alive_count, 'alive')
            # Check how long the game has been waiting for moves on this turn
            time_elapsed = time() - time_start
            if all_moved:
                # Update game state, cleanup player states
                self.update_state()
                # Release threads to make their next moves
                self.move_flag.set()
                self.move_flag.clear()
                # Reset the timer for moves for the next turn
                time_start = time()
            elif time_elapsed > self.bot_timelimit:
                for p in self.players:
                    if not p['did_move'] and self.bot_is_alive(p):
                        # Bots who do not move in time can no longer play
                        p['is_playing'] = False
                        print('Player {} shut down on turn {}.'.format(p['pid'], p['turn']))
            # Check if all threads have finished
            if alive_count == 0:
                self.move_flag.set()
                return
            # Check if max turns have been exceeded:
            turn = max(p['turn'] for p in self.players)
            if turn >= self.max_turns:
                self.move_flag.set()
                return

    def bot_is_alive(self, bot):
        return bot['thread'].is_alive() and bot['is_playing']

    def check_assertions(self):
        # Check that all active players are on the same turn
        max_turn = max(p['turn'] for p in self.players)
        for p in self.players:
            active = self.bot_is_alive(p)
            same_turn = p['turn'] == max_turn
            if active:
                assert same_turn
        # Check that no players share the same position
        for pid, player in enumerate(self.players):
            for o_pid, o_player in enumerate(self.players):
                if pid is not o_pid:
                    same_pos = player['position'] == o_player['position']
                    assert not same_pos

    def update_state(self):
        # Compute desired destination for each player
        destination = [p['position'] for p in self.players]
        for p in self.players:
            if p['did_move']:
                # Inspect move and state of player
                # print('Turn', p['turn'], 'Player', p['pid'], '->', p['move'])
                # Copy position value
                pos = list(p['position'])
                d = p['move']
                pos = self.get_new_position(pos, d)
                # Check if position is in bounds
                if self.is_in_bounds(pos[0], pos[1]):
                    pid = p['pid']
                    destination[pid] = pos
        # Update destinations based on invalid moves
        new_dests = self.get_destinations(destination)
        # Update player positions and paint board
        for pid, dest in enumerate(new_dests):
            self.players[pid]['position'] = dest
            self.board[dest[1]][dest[0]] = str(pid)
        self.update_record(destination)
        # Reset player fields
        for p in self.players:
            p['move'] = None
            p['did_move'] = False
            p['move_failed'] = False
        self.check_assertions()

    def get_destinations(self, destination):
        new_dests = self.prevent_mobile_collisions(destination)
        new_dests = self.prevent_stable_collisions(new_dests)
        return new_dests

    def prevent_mobile_collisions(self, destination):
        # First pass
        new_dests = list(destination)
        for pid, player in enumerate(self.players):
            pos = player['position']
            dest = destination[pid]
            for o_pid, o_player in enumerate(self.players):
                o_pos = o_player['position']
                o_dest = destination[o_pid]
                if pid is not o_pid:
                    # Check for same space
                    if dest == o_dest:
                        new_dests[pid] = pos
                        new_dests[o_pid] = o_pos
                        self.players[pid]['move_failed'] = True
                        self.players[o_pid]['move_failed'] = True
                    # Check for pass throughs
                    if (dest == o_pos) and (o_dest == pos):
                        new_dests[pid] = pos
                        new_dests[o_pid] = o_pos
                        self.players[pid]['move_failed'] = True
                        self.players[o_pid]['move_failed'] = True
        return new_dests

    def prevent_stable_collisions(self, new_dests):
        # Second pass
        for pid, player in enumerate(self.players):
            pos = player['position']
            dest = new_dests[pid]
            still = dest == pos
            if not still:
                for o_pid, o_player in enumerate(self.players):
                    o_pos = o_player['position']
                    o_dest = new_dests[o_pid]
                    o_still = o_dest == o_pos
                    if (pid is not o_pid) and (o_still):
                        # Check for movement into occupied space
                        if dest == o_pos:
                            new_dests[pid] = pos
                            self.players[pid]['move_failed'] = True
        return new_dests

    def get_new_position(self, pos, d):
        if d is not None:
            if d is 'up':
                pos[1] = pos[1] - 1
            if d is 'down':
                pos[1] = pos[1] + 1
            if d is 'left':
                pos[0] = pos[0] - 1
            if d is 'right':
                pos[0] = pos[0] + 1
        return pos

    def is_in_bounds(self, x, y):
        x_legal = x >= 0 and x < len(self.board[0])
        y_legal = y >= 0 and y < len(self.board)
        if x_legal and y_legal:
            return True

    def submit_move(self, pid, direction):
        player = self.players[pid]
        player['turn'] = player['turn'] + 1
        # Inspect that player turn is consistent with game turn
        # print('Turn %d: move by player %d, %s' % (player['turn'], pid, direction))
        self.players[pid]['move'] = direction
        self.players[pid]['did_move'] = True
        # Wait for other players to move
        self.move_flag.wait()

    def print_board(self):
        output = ''
        for row in self.board:
            for cell in row:
                output = output + str(cell) + ' '
            output = output + '\n'
        print(output)

    def get_scores(self):
        scores = [0 for p in self.players]
        for row in self.board:
            for cell in row:
                if cell is not '.':
                    pid = int(cell)
                    scores[pid] = scores[pid] + 1
        return scores

    def get_winners(self):
        winners = []
        high_score = max(self.get_scores())
        for pid, score in enumerate(self.get_scores()):
            if score == high_score:
                winners.append(pid)
        return winners

    def get_turn(self):
        return max(p['turn'] for p in self.players)

    def update_record(self, destination):
        self.record = self.record + ','
        last = len(self.players) - 1
        for pid, player in enumerate(self.players):
            pos = player['position']
            failed = player['move_failed']
            pos_rec = '%d-%d-%d' % (pid, pos[0], pos[1])
            if failed:
                dest = destination[pid]
                pos_rec = '%d-%d-%d-f' % (pid, dest[0], dest[1])
            if pid is not last:
                pos_rec = pos_rec + '!'
            self.record = self.record + pos_rec

    def get_record(self):
        return self.record
