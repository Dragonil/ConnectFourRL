# Connect Four 

## Introduction

Our Project is an AI that plays the game [ConnectFour](https://en.wikipedia.org/wiki/Connect_Four)

### Authors

- Oliver Gorges
- Fabian Stölzle

### Challenges

There are [4531985219092](https://oeis.org/A212693) possible states in the game ConnectFour with a 6x7 grid

    This Results in:
        - A very large set of possible States, which is nearly impossible to discover completely
        - A lot of time to train the AI til it discovered enough states to play against a real Player
        - A lot of storage space is needed to store the Action-Value Function
    


### How to Play

#### Train the AI

Before you can play the game against the AI you should train it at least for `1000000` episodes.

> To play the game without trainig you can also download a [JSON](drive.google.com/file/d/1aWwLZWc6jVqUtHLk88wz48rknHi-ohjI/view?usp=sharing) with trained Data.
> This will not work with Jupyter notebook

#### Start the Game

To play the game against the ai, you have to change the `play` parameter in the `Game Configuration` to True 

When you run now the project it will print the playing Field and you can start playing the game
```bash
    [['-' '-' '-' '-' '-' '-' '-']
     ['-' '-' '-' '-' '-' '-' '-']
     ['-' '-' '-' '-' '-' '-' '-']
     ['-' '-' '-' '-' '-' '-' '-']
     ['-' '-' '-' '-' '-' '-' '-']
     ['-' '-' '-' 'O' '-' '-' '-']]
    -------------------------------
    [['1' '2' '3' '4' '5' '6' '7']]
    Player 2, Enter Postion (1-7): 
```
> When you use oldData it can take a while to load the trained data and display the gamefield

> In the current state of the Project you start always as the secound player, so the ai has done its first turn already.

#### Game Rules

##### Inputs

The player can input a number between 1 and the configured amount of columns (`columns_count`, Default: 7). 
This will place a stone in the first empty row in the selected column.

##### Goal

To win the game you have to create a row out of four stones in a Horizontal, Vertical or Diagonal direction.

```bash
    Horizontal Win
    [['-' '-' '-' '-' '-' '-' '-']
     ['-' '-' '-' '-' '-' '-' '-']
     ['-' '-' '-' 'O' '-' '-' '-']
     ['-' '-' '-' 'O' '-' '-' '-']
     ['-' '-' 'X' 'O' '-' '-' '-']
     ['-' '-' 'X' 'O' '-' '-' 'X']]
    -------------------------------
    [['1' '2' '3' '4' '5' '6' '7']]
    Player 2, Enter Postion (1-7): 
```

```bash
    Vertical Win
    [['-' '-' '-' '-' '-' '-' '-']
     ['-' '-' '-' '-' '-' '-' '-']
     ['-' '-' '-' '-' '-' '-' '-']
     ['-' '-' '-' '-' '-' '-' '-']
     ['-' '-' '-' 'X' 'X' '-' '-']
     ['-' 'O' 'O' 'O' 'O' 'X' '-']]
    -------------------------------
    [['1' '2' '3' '4' '5' '6' '7']]
    Player 2, Enter Postion (1-7): 
```

```bash
    Diagonal Win
    [['-' '-' '-' '-' '-' '-' '-']
     ['-' '-' '-' '-' '-' '-' '-']
     ['-' '-' '-' '-' '-' '-' 'O']
     ['-' '-' '-' '-' '-' 'O' 'X']
     ['-' '-' '-' '-' 'O' 'X' 'X']
     ['-' '-' 'O' 'O' 'X' 'O' 'X']]
    -------------------------------
    [['1' '2' '3' '4' '5' '6' '7']]
    Player 2, Enter Postion (1-7): 
```

> The amount of stones to win can be changed by changing the parameter `terminating_length`
