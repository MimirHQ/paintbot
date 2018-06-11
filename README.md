# PaintBot
Program bots and compete to cover the playing field in your color.

## Try It

You can play PaintBot [at this link](https://repl.it/@vingkan/paintbotpython) (no account creation required).

See a sample game replay [at this link](https://paintbot.glitch.me/?s=6,6,0-0-0!1-5-5!2-0-5,0-0-1!1-5-4!2-0-5,0-0-2!1-5-3!2-0-4,0-0-3!1-4-3!2-1-4,0-1-3!1-3-3!2-1-4,0-2-3-f!1-2-3-f!2-1-4,0-2-3-f!1-2-3-f!2-1-3-f,0-1-3!1-3-3!2-1-4).

## Learning Objectives

- Evaluate Python programs in your head while reading source code.
- Write Python programs using loops and conditionals.

## Instructions

Every player in PaintBot programs their strategy through a method that takes a single argument. The `bot` parameter is a PaintBot object containing many methods for game play.

Read [the documentation](docs.md) to read the rules see what methods can be used.

See `examplegame.py` for a sample game with two sample players, all defined in a single file.

Consider this short, example player code:

```python
def main(bot):
    """Your player strategy"""
    while bot.is_playing():
        bot.right()
```

## Contributions

If you create a bot player that you want to share with the community, you can [create a pull request](https://help.github.com/articles/creating-a-pull-request/) and add it to this repository in the `community` folder. Community bots must meet these requirements:

- [x] Can be used by any teachers or learners for free
- [x] Uses a filename that is not already taken
- [x] Includes the author's name, screen name, website link, or other means through which they want to be credited
- [x] (Preferably) Is contained within a single file, with minimal or no public package dependencies

If this is your first time creating a pull request or you have other questions, feel free to contact the maintainer:

- Vinesh Kannan
- vinesh [at] mimirhq [dot] com

## About

This project is, in part, inspired by a mini game from Mario Party and the video game series Splatoon. These projects are not affiliated.

PaintBot is maintained by the curriculum team at [Mimir](https://www.mimirhq.com/), a company that helps high schools and universities teach computer science classes and give their students helpful feedback on their work.
