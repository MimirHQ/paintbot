"""This sample game illustrates the collision rules in PaintBot. Written by the Mimir curriculum team."""

from paintbot import (
    PaintGame
)


def p0_main(bot):
    bot.down()
    bot.down()
    bot.down()
    bot.right()
    bot.right()


def p1_main(bot):
    bot.up()
    bot.up()
    bot.left()
    bot.left()
    bot.left()


def p2_main(bot):
    bot.up()
    while True:
        pass
    bot.right()
    bot.skip()
    bot.skip()
    bot.up()


X = 6
Y = 6
game = PaintGame(X, Y, max_turns=10, bot_timelimit=1)
game.add_player(p0_main, [0, 0])
game.add_player(p1_main, [X - 1, Y - 1])
game.add_player(p2_main, [0, Y - 1])
game.start()
game.print_board()
print('Final Score:', game.get_scores())
print('Winners:', game.get_winners())
record = game.get_record()
print('https://paintbot.glitch.me?s=%s' % record)
