# PaintBot Documentation

Program your robot to compete with other players and cover the virtual playing field in your color of paint.

## Rules

- Bots paint any cell they occupy in their own color
- When the game starts, bots paint their starting cell in their own color.
- On each turn, all bots move at the same time.
- Bots can move up, down, left, or right.
- Bots can skip a turn instead of moving.
- Bots cannot move into a cell occupied by another bot.
- If multiple bots try to move into the same cell, they will all stay on their original cells.
- Bots start the game facing in the up direction.
- Bots face the direction of their last move.

## PaintBot API

### Movement

Calling any of these methods uses a turn.

#### bot.up()

- Moves the bot up (towards y = 0), if possible
- Makes the bot face in the `'up'` direction

#### bot.down()

- Moves the bot down (away from y = 0), if possible
- Makes the bot face in the `'down'` direction

#### bot.left()

- Moves the bot left (towards x = 0), if possible
- Makes the bot face in the `'left'` direction

#### bot.right()

- Moves the bot right (away from x = 0), if possible
- Makes the bot face in the `'right'` direction

#### bot.skip()

- Skips the current turn

### Sensors

Calling any of these methods **does not** use a turn.

#### bot.face(direction)

- Parameter `direction`: `string` the direction in which to face (`'up'`, `'down'`, `'left'`, or `'right'`)

#### bot.is_blocked()

- Returns: `boolean` `True` if the bot cannot move in the direction it is currently facing, `False` otherwise

### Accessing Game Data

Calling any of these methods **does not** use a turn.

#### bot.get_x_size()

- Returns: `int` the width of the playing field

#### bot.get_y_size()

- Returns: `int` the height of the playing field

#### bot.get_turn()

- Returns: `int` the turn number, starting from zero

#### bot.get_max_turns()

- Returns: `int` the maximum number of turns in the game

#### bot.is_playing()

- Returns: `bool` `True` if the game is not over, `False` otherwise

#### bot.get_number_of_players()

- Returns: `int` the number of players in the game

#### bot.get_my_score()

- Returns: `int` the number of cells currently in your color

#### bot.get_player_score(pid)

- Parameter `pid`: `int` player id
- Returns: `int` the number of cells currently in the color of the player with the given id

#### bot.get_my_position()

- Returns: `list` a list of two integers representing your current x and y position on the playing field

#### bot.get_player_position(pid)

- Parameter `pid`: `int` player id
- Returns: `list` a list of two integers representing the current x and y position on the playing field of the player with the given id

#### bot.get_my_color()

- Returns: `int` a number representing your color

#### bot.get_cell_color(x, y)

- Parameter `x`: `int` the x coordinate of a cell
- Parameter `y`: `int` the y coordinate of a cell
- Returns: `int` a number representing the color of the cell at the given coordinates

#### bot.cell_is_occupied(x, y)

- Parameter `x`: `int` the x coordinate of a cell
- Parameter `y`: `int` the y coordinate of a cell
- Returns: `bool` `True` if there is an occupied cell at the given coordinates, `False` otherwise

#### bot.cell_is_in_bounds(x, y)

- Parameter `x`: `int` the x coordinate of a cell
- Parameter `y`: `int` the y coordinate of a cell
- Returns: `bool` `True` if there is a cell at the given coordinates within the playing field, `False` otherwise
