from flask import Flask
import random

ocean1 = [['0' for _ in range(10)] for _ in range(10)]
ocean2 = [['0' for _ in range(10)] for _ in range(10)]

header = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

ships = ['acarrier', 'battleship', 'cruiser', 'submarine', 'destroyer']

ship_lengths = {
    'acarrier': 5,
    'battleship': 4,
    'cruiser': 3,
    'submarine': 3,
    'destroyer': 2
}

def print_ocean(ocean):
    header = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    print("   " + " ".join(header))  # Print column labels

    for i, row in enumerate(ocean, start=1):
        row_str = " ".join(row)
        print(f"{i:2d} {row_str}")

def is_adjacent(matrix, row, col):
    adjacent_positions = [
        (row - 1, col), (row + 1, col),
        (row, col - 1), (row, col + 1),
        (row - 1, col - 1), (row - 1, col + 1),
        (row + 1, col - 1), (row + 1, col + 1)
    ]

    for r, c in adjacent_positions:
        if 0 <= r < len(matrix) and 0 <= c < len(matrix[0]):
            if matrix[r][c] != '0':
                return True

    return False

def place_ship(matrix, ship_length):
    while True:
        orientation = random.choice(['horizontal', 'vertical'])
        if orientation == 'horizontal':
            row = random.randint(0, 9)
            col = random.randint(0, 10 - ship_length)
        else:
            row = random.randint(0, 10 - ship_length)
            col = random.randint(0, 9)

        valid = True
        for i in range(ship_length):
            if orientation == 'horizontal':
                if matrix[row][col + i] != '0' or is_adjacent(matrix, row, col + i):
                    valid = False
                    break
            else:
                if matrix[row + i][col] != '0' or is_adjacent(matrix, row + i, col):
                    valid = False
                    break

        if valid:
            break

    return row, col, orientation

def shoot(matrix, row, col):
    if matrix[row][col] == 'm':
        return False  # Already shot at this square
    elif matrix[row][col] != '0':
        matrix[row][col] = 'x'
        return True  # Hit!
    else:
        matrix[row][col] = 'm'  # Miss
        return False


def makeocean1():
    for ship in ships:
        ship_length = ship_lengths[ship]
        row, col, orientation = place_ship(ocean1, ship_length)

        if orientation == 'horizontal':
            for i in range(ship_length):
                ocean1[row][col + i] = ship[0]
                if i < ship_length - 1:
                    ocean1[row][col + i + 1] = 'X'  # Mark adjacent positions
        else:
            for i in range(ship_length):
                ocean1[row + i][col] = ship[0]
                if i < ship_length - 1:
                    ocean1[row + i + 1][col] = 'X'  # Mark adjacent positions
def makeocean2():
    for ship in ships:
        ship_length = ship_lengths[ship]
        row, col, orientation = place_ship(ocean2, ship_length)

        if orientation == 'horizontal':
            for i in range(ship_length):
                ocean2[row][col + i] = ship[0]
                if i < ship_length - 1:
                    ocean2[row][col + i + 1] = 'X'  # Mark adjacent positions
        else:
            for i in range(ship_length):
                ocean2[row + i][col] = ship[0]
                if i < ship_length - 1:
                    ocean2[row + i + 1][col] = 'X'  # Mark adjacent positions

def htmlocean(ocean):
    mstr = "<table><tr><td></td><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td><td>F</td><td>G</td><td>H</td><td>I</td><td>J</td></tr>"
    for i, row in enumerate(ocean, start=1):
        mstr = mstr + "<tr><td>" + str(i) + "</td>"        
        for r in row:
            mstr = mstr + "<td>"+r+"</td>"
        mstr = mstr + "</tr>"
    mstr = mstr + "</table>"
    return mstr

app = Flask(__name__)

makeocean1()
makeocean2()

@app.route('/')
def start():
    p1oceanstr = htmlocean(ocean1)
    p2oceanstr = htmlocean(ocean2)
    mstr = "Player 1 ocean <br>"+p1oceanstr+"<br>Player 2 ocean <br>"+p2oceanstr+"<br>"
    mstr = mstr + "<form method='GET'>ROW <input name='R'>COL <input name='C'> <input type='submit' value='Submit'></form>" 
    return mstr


app.run(host='0.0.0.0') 



print("   " + " ".join(header))  # Print header for ocean1
for i, row in enumerate(ocean1, start=1):
    row_str = " ".join(row)
    print(f"{i:2d} {row_str}")  # Print line number and row content

print("\nPlayer 2's Ocean:")
print("   " + " ".join(header))  # Print header for ocean2
for i, row in enumerate(ocean2, start=1):
    row_str = " ".join(row)
    print(f"{i:2d} {row_str}")  # Print line number and row content for ocean2

current_player = 1
while any(ship[0] in row for row in ocean1 for ship in ships) and any(ship[0] in row for row in ocean2 for ship in ships):
        if current_player == 1:
            print("Player 1's turn")
            print_ocean(ocean1)
            row = int(input("Enter row number (1-10): ")) - 1
            col = ord(input("Enter column letter (A-J): ").upper()) - ord('A')
            if 0 <= row < 10 and 0 <= col < 10:
                if shoot(ocean2, row, col):
                    print("Hit!")
                else:
                    print("Miss!")
                current_player = 2
            else:
                print("Invalid input. Try again.")
        else:
            print("Player 2's turn (Computer)")
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if shoot(ocean1, row, col):
                print(f"Computer hit at {chr(col + ord('A'))}{row + 1}!")
            else:
                print(f"Computer missed at {chr(col + ord('A'))}{row + 1}!")
            current_player = 1

if not any(ship[0] in row for row in ocean2 for ship in ships):
            print("Player 1 wins!")
else:
            print("Player 2 (Computer) wins!")
  