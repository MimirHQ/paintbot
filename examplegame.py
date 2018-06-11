from paintbot import PaintGame


def main_player0(bot):
  """Player 0 Strategy"""
  arena_size = bot.get_x_size()
  while bot.is_playing():
      for i in range(arena_size):
          bot.right()
      for j in range(arena_size):
          bot.left()


def main_player1(bot):
  """Player 1 Strategy"""
  arena_size = bot.get_x_size()
  while bot.is_playing():
      for j in range(arena_size):
          bot.down()
      for j in range(arena_size):
          bot.left()
      for j in range(arena_size):
          bot.up()
      for i in range(arena_size):
          bot.right()


X = 5
Y = 5
game = PaintGame(X, Y)
game.add_player(main_player0, [0, 0])
game.add_player(main_player1, [X - 1, 0])
game.start()
game.print_board()
print('Final Score:', game.get_scores())
print('Winners:', game.get_winners())
record = game.get_record()
print('\nView Replay:')
print('https://paintbot.glitch.me?s=%s' % record)
