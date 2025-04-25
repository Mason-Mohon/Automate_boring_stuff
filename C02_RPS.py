import random, sys
from C03_zigzag import zigzag

print("ROCK, PAPER, SCISSORS!")

#Variables to keep track of wins, losses, and ties
wins = 0
losses = 0
ties = 0

while True: #Main game loop
    print("%s Wins, %s Losses, %s Ties" % (wins, losses, ties))
    while True: #player input loop
        print("Enter your move: r, p, s, or q for quit")
        playerMove = input()
        if playerMove == 'q':
            sys.exit() #quits the program
        if playerMove in ["r","p","s"]:
            break
        print("Type r, p, s, or q")

    #Display player choice
    if playerMove == 'r':
        print("ROCK versus...")
    elif playerMove == 'p':
        print("PAPER versus...")
    elif playerMove == 's':
        print("SCISSORS versus...")

    #Display what computer chose
    randomNumber = random.randint(1, 3)
    if randomNumber == 1:
        computerMove = 'r'
        print("ROCK")
    if randomNumber == 2:
        computerMove = 'p'
        print("PAPER")
    if randomNumber == 3:
        computerMove = 's'
        print("SCISSORS")

    #Display and record round results
    if playerMove == computerMove:
        print('Tie')
        ties += 1
    elif (playerMove == 'r' and computerMove == 's') or (playerMove == 's' and computerMove == 'p') or (playerMove == 'p' and computerMove == 'r'):
        print("You win!")
        wins+=1
    else:
        print("You lose!")
        losses += 1