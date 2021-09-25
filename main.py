from random import randint, choice, seed
import time

import game as game


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_field(field, n, m, flags):
    for i in range(n):
        if i == 0:
            line_n = "\t" + bcolors.OKCYAN + "\t".join([str(k) for k in range(m)])
            print(line_n)
        line = bcolors.OKCYAN + str(i) + "\t" + bcolors.ENDC
        for j in range(m):
            if [j, i] in flags:
                line += bcolors.FAIL + "!" + bcolors.ENDC + "\t"
            elif field[i][j] == "." or field[i][j] == "*":
                line += "#" + "\t"
            elif field[i][j] == "Q":
                line += "." + "\t"
            else:
                line += str(field[i][j]) + "\t"

        print(line)


def print_field_lose(field, n, m):
    for i in range(n):
        if i == 0:
            line_n = "\t" + bcolors.OKCYAN + "\t".join([str(k) for k in range(m)])
            print(line_n)
        line = bcolors.OKCYAN + str(i) + "\t" + bcolors.ENDC
        for j in range(m):
            if field[i][j] == "Q":
                line += "." + "\t"
            elif field[i][j] == "*":
                line += bcolors.FAIL + field[i][j] + bcolors.ENDC + "\t"
            else:
                line += field[i][j] + "\t"
        print(line)


def print_field_debug(field, n, m):
    for i in range(n):
        if i == 0:
            line_n = "\t" + "\t".join([str(k) for k in range(m)])
            print(line_n)
        line = str(i) + "\t"
        for j in range(m):
            line += field[i][j] + "\t"
        print(line)


def create_field(field_a, n, m, count_min, count_max, not_x, not_y, game_seed):
    bombs_count_a = 0
    seed(game_seed)
    while True:
        for i in range(n):
            for j in range(m):
                if i != not_y and j != not_x:
                    rand = randint(0, n * m)
                    if rand <= count_max and bombs_count_a < count_max:
                        field_a[i][j] = "*"
                        bombs_count_a += 1
        if bombs_count_a >= count_min:
            break
    return field_a


def check_for_bombs(field_a, n, m, x_a, y_a, checked):
    bombs_count_a = count_bombs(field_a, n, m, x_a, y_a)
    if bombs_count_a == 0 and [x_a, y_a] not in checked and field_a[y_a][x_a] != "*":
        field_a, checked = open_cells(field_a, n, m, x_a, y_a, checked)
    else:
        if field_a[y_a][x_a] != "*" and bombs_count_a != 0:
            field_a[y_a][x_a] = str(bombs_count_a)
    return field_a, checked


def open_cells(field_a, n, m, x_a, y_a, checked=[]):
    checked.append([x_a, y_a])
    if x_a - 1 >= 0:
        field_a, checked = check_for_bombs(field_a, n, m, x_a - 1, y_a, checked)
        if y_a - 1 >= 0:
            field_a, checked = check_for_bombs(field_a, n, m, x_a - 1, y_a - 1, checked)
        if y_a + 1 < n:
            field_a, checked = check_for_bombs(field_a, n, m, x_a - 1, y_a + 1, checked)
    if x_a + 1 < m:
        field_a, checked = check_for_bombs(field_a, n, m, x_a + 1, y_a, checked)
        if y_a - 1 >= 0:
            field_a, checked = check_for_bombs(field_a, n, m, x_a + 1, y_a - 1, checked)
        if y_a + 1 < n:
            field_a, checked = check_for_bombs(field_a, n, m, x_a + 1, y_a + 1, checked)
    if y_a - 1 >= 0:
        field_a, checked = check_for_bombs(field_a, n, m, x_a, y_a - 1, checked)
    if y_a + 1 < n:
        field_a, checked = check_for_bombs(field_a, n, m, x_a, y_a + 1, checked)
    field_a[y_a][x_a] = "Q"
    return field_a, checked


def check_for_win(field_a, n, m):
    win = True
    for i in range(n):
        for j in range(m):
            if field_a[i][j] == ".":
                win = False
                break
        if not win:
            break
    return win


def count_bombs(field_a, n, m, x_a, y_a):
    bombs_count_a = 0
    if x_a - 1 >= 0:
        if field_a[y_a][x_a - 1] == "*":
            bombs_count_a += 1
        if y_a - 1 >= 0:
            if field_a[y_a - 1][x_a - 1] == "*":
                bombs_count_a += 1
        if y_a + 1 < n:
            if field_a[y_a + 1][x_a - 1] == "*":
                bombs_count_a += 1
    if x_a + 1 < m:
        if field_a[y_a][x_a + 1] == "*":
            bombs_count_a += 1
        if y_a - 1 >= 0:
            if field_a[y_a - 1][x_a + 1] == "*":
                bombs_count_a += 1
        if y_a + 1 < n:
            if field_a[y_a + 1][x_a + 1] == "*":
                bombs_count_a += 1
    if y_a - 1 >= 0:
        if field_a[y_a - 1][x_a] == "*":
            bombs_count_a += 1
    if y_a + 1 < n:
        if field_a[y_a + 1][x_a] == "*":
            bombs_count_a += 1
    return bombs_count_a


def count_probability(field, n, m):
    probability_field = [[0 for i in range(m)] for j in range(n)]
    for y_a in range(n):
        for x_a in range(m):
            if '1' <= field[y_a][x_a] <= '9':
                if x_a - 1 >= 0:
                    if field[y_a][x_a - 1] == "." or field[y_a][x_a - 1] == "*":
                        probability_field[y_a][x_a - 1] += int(field[y_a][x_a])
                    else:
                        probability_field[y_a][x_a - 1] = -1
                    if y_a - 1 >= 0:
                        if field[y_a - 1][x_a - 1] == "." or field[y_a - 1][x_a - 1] == "*":
                            probability_field[y_a - 1][x_a - 1] += int(field[y_a][x_a])
                        else:
                            probability_field[y_a - 1][x_a - 1] = -1
                    if y_a + 1 < n:
                        if field[y_a + 1][x_a - 1] == "." or field[y_a + 1][x_a - 1] == "*":
                            probability_field[y_a + 1][x_a - 1] += int(field[y_a][x_a])
                        else:
                            probability_field[y_a + 1][x_a - 1] = -1
                if x_a + 1 < m:
                    if field[y_a][x_a + 1] == "." or field[y_a][x_a + 1] == "*":
                        probability_field[y_a][x_a + 1] += int(field[y_a][x_a])
                    else:
                        probability_field[y_a][x_a + 1] = -1
                    if y_a - 1 >= 0:
                        if field[y_a - 1][x_a + 1] == "." or field[y_a - 1][x_a + 1] == "*":
                            probability_field[y_a - 1][x_a + 1] += int(field[y_a][x_a])
                        else:
                            probability_field[y_a - 1][x_a + 1] = -1
                    if y_a + 1 < n:
                        if field[y_a + 1][x_a + 1] == "." or field[y_a + 1][x_a + 1] == "*":
                            probability_field[y_a + 1][x_a + 1] += int(field[y_a][x_a])
                        else:
                            probability_field[y_a + 1][x_a + 1] = -1
                if y_a - 1 >= 0:
                    if field[y_a - 1][x_a] == "." or field[y_a - 1][x_a] == "*":
                        probability_field[y_a - 1][x_a] += int(field[y_a][x_a])
                    else:
                        probability_field[y_a - 1][x_a] = -1
                if y_a + 1 < n:
                    if field[y_a + 1][x_a] == "." or field[y_a + 1][x_a] == "*":
                        probability_field[y_a + 1][x_a] += int(field[y_a][x_a])
                    else:
                        probability_field[y_a + 1][x_a] = -1
                probability_field[y_a][x_a] = -1
    for y_a in range(n):
        for x_a in range(m):
            if probability_field[y_a][x_a] == 0:
                probability_field[y_a][x_a] = -1

    return probability_field


def choose_step(probability_field, n, m):
    m_min = 15
    posible_steps = []
    for i in range(n):
        values = [j for j in probability_field[i] if j > 0]
        if len(values) > 0:
            line_min = min(values)
            if line_min < m_min:
                m_min = line_min
    for i in range(n):
        for j in range(n):
            if probability_field[i][j] == m_min:
                posible_steps.append([j, i])
    return choice(posible_steps)


def load_game(save_name, n, m, count_min, count_max):
    print("Game loading...")
    with open(save_name + ".save", 'r') as f:
        i = 0
        flags = []
        game_seed = 0
        field = [["." for i in range(m)] for j in range(n)]
        for line in f:
            if i == 0:
                game_seed = float(line)
            else:
                com = line.split()
                if com[2] == "s":
                    not_x = int(com[1])
                    not_y = int(com[0])
                    field = create_field(field, n, m, count_min, count_max, not_x, not_y, game_seed)
                elif com[2] == "!":
                    flags.append([int(com[1]), int(com[0])])
                else:
                    x = int(com[1])
                    y = int(com[0])
                    field[y][x] = com[2]
            i += 1
        print("Game loaded!")
        return flags, field, game_seed


def save_game(field, n, m, game_seed, save_name, flags, n_x, n_y):
    with open(save_name + ".save", 'w') as f:
        f.write(str(game_seed))
        f.write(f"\n{n_y} {n_x} s")
        for i in range(n):
            for j in range(m):
                if field[i][j] == "Q" or '1' <= field[i][j] <= '9':
                    f.write(f"\n{i} {j} {field[i][j]}")
        for flag in flags:
            f.write(f"\n{flag[1]} {flag[0]} !")
    print("Game saved!")


n = 5
m = 5
my_seed = time.time()
seed(my_seed)
bombs_count_min = 2
bombs_count_max = 5
not_x, not_y = 0, 0
instructions = """Welcome to the bombs game.
There is 3 types of game:
Play(Play yourself)
Load(Load saved game)
PCRT(PC rate test)
PC(PC playing)
"""
print(instructions)
game_type = input("Enter game type: ")
if game_type == "Play" or game_type == "Load":
    if game_type == "Load":
        save_name = input("Save name:")
        flags, field, my_seed = load_game(save_name, n, m, bombs_count_min, bombs_count_max)
        print_field(field, n, m, flags)
    else:
        instructions = """The field is generated.
           To Open the cell enter "x y Open"
           To put a flag enter "x y Flag"
           To get a probability field enter "0 0 hint"
           To save game enter "0 0 Save"
           """
        print(instructions)
        flags = []
        field = [["." for i in range(m)] for j in range(n)]
        print_field(field, n, m, [])
        command = input(bcolors.OKGREEN + "Enter command: " + bcolors.ENDC).split()
        x = int(command[0])
        y = int(command[1])
        not_x, not_y = x, y
        field = create_field(field, n, m, bombs_count_min, bombs_count_max, x, y, my_seed)
        bombs_count = count_bombs(field, n, m, x, y)
        if bombs_count == 0:
            open_cells(field, n, m, x, y)
        else:
            field[y][x] = str(bombs_count)
        print_field(field, n, m, flags)

    while True:
        command = input(bcolors.OKGREEN + "Enter command: " + bcolors.ENDC).split()
        x = int(command[0])
        y = int(command[1])
        if len(command) != 3:
            print(bcolors.FAIL + "Unknown command! Retry!" + bcolors.ENDC)
            continue
        if command[2] == "Flag":
            flags.append([x, y])
        elif command[2] == "Open":
            if [x, y] in flags:
                flags.remove([x, y])
            if field[y][x] == "*":
                print("=" * 50)
                print("=" * 50)
                print("=" * 50)
                print(bcolors.FAIL + "YOU LOSE!" + bcolors.ENDC)
                print("=" * 50)
                print("=" * 50)
                print("=" * 50)
                print_field_lose(field, n, m)
                print("=" * 50)
                print("=" * 50)
                print("=" * 50)
                break
            bombs_count = count_bombs(field, n, m, x, y)
            if bombs_count == 0:
                open_cells(field, n, m, x, y)
            else:
                field[y][x] = str(bombs_count)
        elif command[2] == "hint":
            probability_field = count_probability(field, n, m)
            print_field(probability_field, n, m, [])
        elif command[2] == "Save":
            save_name = input("Enter save name: ")
            save_game(field, n, m, my_seed, save_name, flags, not_x, not_y)
            break
        else:
            print(bcolors.FAIL + "Unknown command! Retry!" + bcolors.ENDC)
            continue
        print_field(field, n, m, flags)
        print("-" * 50)
        win = check_for_win(field, n, m)
        if win:
            print("=" * 50)
            print("=" * 50)
            print("=" * 50)
            print(bcolors.OKBLUE + "YOU WIN!" + bcolors.ENDC)
            print("=" * 50)
            print("=" * 50)
            print("=" * 50)
            break

elif game_type == "PCRT":
    win_games = 0
    all = int(input("Enter count of games:"))
    maked = 0
    x = randint(0, m - 1)
    y = randint(0, n - 1)
    field = [["." for i in range(m)] for j in range(n)]
    steps = 0
    for k in range(all):
        x = 0
        y = 0
        my_seed = time.time()
        field = [["." for i in range(m)] for j in range(n)]
        field = create_field(field, n, m, bombs_count_min, bombs_count_max, x, y, my_seed)
        bombs_count = count_bombs(field, n, m, x, y)
        if bombs_count == 0:
            open_cells(field, n, m, x, y, [])
        else:
            field[y][x] = str(bombs_count)
        probability_field = count_probability(field, n, m)
        while True:
            x, y = choose_step(probability_field, n, m)
            if field[y][x] == "*":
                print(bcolors.FAIL + "LOSE!" + bcolors.ENDC)
                break
            bombs_count = count_bombs(field, n, m, x, y)
            if bombs_count == 0:
                open_cells(field, n, m, x, y)
            else:
                field[y][x] = str(bombs_count)
            win = check_for_win(field, n, m)
            if win:
                print(bcolors.OKBLUE + "WIN!" + bcolors.ENDC)
                win_games += 1
                break
            probability_field = count_probability(field, n, m)
            steps += 1
        maked += 1
        print(k + 1, "games played")
    print("Games wined:", win_games, "Games was:", maked, "Winrate: ", float(win_games) / float(maked))
    print("Mean steps:", steps / maked)
elif game_type == "PC":
    x = randint(0, m - 1)
    y = randint(0, n - 1)
    field = [["." for i in range(m)] for j in range(n)]
    field = create_field(field, n, m, bombs_count_min, bombs_count_max, x, y, my_seed)
    print_field_lose(field, n, m)
    print("-" * 50)
    print_field(field, n, m, [])
    print("-" * 50)
    bombs_count = count_bombs(field, n, m, x, y)
    if bombs_count == 0:
        open_cells(field, n, m, x, y, [])
    else:
        field[y][x] = str(bombs_count)
    probability_field = count_probability(field, n, m)
    while True:
        print_field(field, n, m, [])
        x, y = choose_step(probability_field, n, m)
        print(f"Computer choosed x={x} y={y}")
        if field[y][x] == "*":
            print(bcolors.FAIL + "LOSE!" + bcolors.ENDC)
            break
        bombs_count = count_bombs(field, n, m, x, y)
        if bombs_count == 0:
            open_cells(field, n, m, x, y)
        else:
            field[y][x] = str(bombs_count)
        win = check_for_win(field, n, m)
        if win:
            print(bcolors.OKBLUE + "WIN!" + bcolors.ENDC)
            break
        probability_field = count_probability(field, n, m)
