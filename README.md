# Janggi

Janggi, sometimes called Korean chess, is a strategy board game popular in Korea. The game was derived from xiangqi (Chinese chess) of China and is very similar to it, including the starting position of the pieces, and the 9×10 gameboard, but without the xiangqi "river" dividing the board horizontally in the middle.

Janggi is played on a board nine lines wide by ten lines long. The game is sometimes fast paced due to the jumping cannons and the long-range elephants, but professional games most often last over 150 moves and so are typically slower than those of Western chess.

source: [Wikipedia](https://en.wikipedia.org/wiki/Janggi)

# About

This program is written in Python. No modules or packages are used in the program. Currently the game can only be played via text, a gui may be impemented in the future.

# How to Play

Example:

```python
g = JanggiGame() #initialize game
g.make_move('c10','d8') #blue horse moves
g.make_move('c1','d3') #red horse moves
g.make_move('e7','e6') #blue soldier
g.make_move('e4','e5') #red
g.make_move('c7','c6') #blue
g.make_move('c4','c5') #red
g.make_move('c6','c5') #blue soldier captures red
g.make_move('e5','e6') #red soldier captures blue
```

## License
[MIT](https://choosealicense.com/licenses/mit/)