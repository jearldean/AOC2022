import collections
from anytree import Node, RenderTree
import pprint

day = 1
dev_env = True


def run_all_days(up_until_day):
    for run_day in range(1, up_until_day + 1):
        run_one_day(run_day)


def run_one_day(run_day, include_prod=False):
    global day
    global dev_env
    day = run_day

    dev_env = True
    print(color_me(f"Day {run_day}:", "Green"), color_me("Sample Puzzle Input (DEV)", "Blue"))
    execute()
    print()

    if include_prod:
        dev_env = False
        print(color_me(f"Day {run_day}:", "Green"), color_me("My Puzzle Input (PROD)", "Red"))
        execute()
        print()

    print()


def execute():
    globals()[f"day{day}"]()


def import_data(day: int, dev_env: bool = True, strip: bool = True):
    folder = 'DEV' if dev_env else "PROD"
    data_path = f"{folder}/{day}.txt"
    data_pack = []
    f = open(data_path)
    for line in f:
        if strip:
            data_pack.append(line.strip())
        else:
            data_pack.append(line)
    return data_pack


def color_me(string, color):
    terminal_colors = {"Black": "\u001b[30",
                       "Red": "\u001b[31m",
                       "Green": "\u001b[32m",
                       "Yellow": "\u001b[33m",
                       "Blue": "\u001b[34m",
                       "Magenta": "\u001b[35m",
                       "Cyan": "\u001b[36m",
                       "White": "\u001b[37m",
                       "Reset": "\u001b[0m"}
    reset = terminal_colors["Reset"]
    error_color = terminal_colors["Red"]
    try:
        return f"{terminal_colors[color]}{string}{reset}"
    except KeyError:
        dict_keys_ = terminal_colors.keys()
        allowed_colors = {str(key) for key in dict_keys_}
        print(f"{error_color}Oops, I don't have the color '{color}' in my databanks. "
              f"I only have {allowed_colors}{reset}")
        return string


def error_checker(value, dev_should_be, prod_should_be):
    error_message = ""
    if dev_env and value != dev_should_be:
        error_message = color_me(f"\t{value} should be {dev_should_be}.", "Red")
    if not dev_env and value != prod_should_be:
        error_message = color_me(f"\t{value} should be {prod_should_be}.", "Red")
    return error_message


def day1():
    data_pack = import_data(day, dev_env)
    answer_units = "rucksack calories"
    elf_stores = []

    running_total = 0
    for food_unit in data_pack:
        if not food_unit:
            elf_stores.append(running_total)
            running_total = 0  # Reset it for the next food pack.
        else:
            running_total += int(food_unit)
    elf_stores.append(running_total)  # Tack on the last guy.

    elf_stores.sort(reverse=True)
    silver_star_answer = elf_stores[0]
    print("Ag*:", silver_star_answer, answer_units,
          error_checker(silver_star_answer, 24000, 67622))
    gold_star_answer = elf_stores[0] + elf_stores[1] + elf_stores[2]
    print("Au*:", gold_star_answer, answer_units,
          error_checker(gold_star_answer, 45000, 201491))


def day2():
    # https://adventofcode.com/2022/day/2
    data_pack = import_data(day, dev_env)
    answer_units = "rock-paper-scissors score"
    overall_score1 = 0
    overall_score2 = 0
    for i in data_pack:
        first, second = i.split(" ")
        overall_score1 += rock_paper_scissors1(hers=first, mine=second)
        overall_score2 += rock_paper_scissors2(hers=first, outcome_code=second)

    print("Ag*:", overall_score1, answer_units,
          error_checker(overall_score1, 15, 10994))
    print("Au*:", overall_score2, answer_units,
          error_checker(overall_score2, 12, 12526))


def rock_paper_scissors1(hers, mine):
    if (hers == "A" and mine == "X") or (hers == "B" and mine == "Y") or (
            hers == "C" and mine == "Z"):
        outcome = "draw"
    elif (hers == "A" and mine == "Y") or (hers == "B" and mine == "Z") or (
            hers == "C" and mine == "X"):
        outcome = "win"
    elif (hers == "A" and mine == "Z") or (hers == "B" and mine == "X") or (
            hers == "C" and mine == "Y"):
        outcome = "lose"

    return scorer(mine, outcome)


def rock_paper_scissors2(hers, outcome_code):
    """Anyway, the second column says how the round needs to end: X means you need to lose,
    Y means you need to end the round in a draw, and Z means you need to win."""
    if outcome_code == "X":
        outcome = "lose"
        correspondo_dict = {"A": "Z", "B": "X", "C": "Y"}
        mine = correspondo_dict[hers]
    elif outcome_code == "Y":
        outcome = "draw"
        correspondo_dict = {"A": "X", "B": "Y", "C": "Z"}
        mine = correspondo_dict[hers]
    elif outcome_code == "Z":
        outcome = "win"
        correspondo_dict = {"A": "Y", "B": "Z", "C": "X"}
        mine = correspondo_dict[hers]

    return scorer(mine, outcome)


def scorer(my_play, outcome):
    """The score for a single round is the score for the shape you selected
    (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome
    of the round (0 if you lost, 3 if the round was a draw, and 6 if you won)."""
    score = 0
    if my_play == "X":
        score += 1
    if my_play == "Y":
        score += 2
    if my_play == "Z":
        score += 3
    if outcome == "win":
        score += 6
    if outcome == "lose":
        score += 0
    if outcome == "draw":
        score += 3
    return score


def day3():
    data_pack = import_data(day, dev_env)
    answer_units = "rucksack item count"
    sum_the_priorities = 0
    for rucksack in data_pack:
        pouch_item_count = int(len(rucksack) / 2)
        dupe_item = find_the_dupe_item(
            [rucksack[:pouch_item_count], rucksack[pouch_item_count:]])
        if dupe_item:
            sum_the_priorities += get_priority(char=dupe_item)
    print("Ag*:", sum_the_priorities, answer_units,
          error_checker(sum_the_priorities, 157, 8053))

    sum_the_priorities = 0
    for elf_group_number in range(1, int((len(data_pack) / 3) + 1)):
        elf_group_set = elf_group_number * 3
        elf_group_packs = [data_pack[elf_group_set - 3], data_pack[elf_group_set - 2],
                           data_pack[elf_group_set - 1]]
        dupe_item = find_the_dupe_item(elf_group_packs)
        sum_the_priorities += get_priority(char=dupe_item)
    print("Au*:", sum_the_priorities, answer_units,
          error_checker(sum_the_priorities, 70, 2425))


def find_the_dupe_item(list_of_contents):
    for candidate_char in list_of_contents[0]:
        matching_list_members = [i for i in list_of_contents[1:] if candidate_char in i]
        if len(matching_list_members) == len(list_of_contents) - 1:  # Everyone matched
            return candidate_char


def get_priority(char):
    offset = -96 if char == char.lower() else -38
    return ord(char) + offset


def day4():
    data_pack = import_data(day, dev_env)
    answer_units = "overlapping pairs"
    total_encompasing_pairs = 0
    partial_encompasing_pairs = 0
    for elf_pairing in data_pack:
        range1 = list(range(int(elf_pairing.split(",")[0].split("-")[0]),
                            int(elf_pairing.split(",")[0].split("-")[1]) + 1))
        range2 = list(range(int(elf_pairing.split(",")[1].split("-")[0]),
                            int(elf_pairing.split(",")[1].split("-")[1]) + 1))
        if all(elem in range1 for elem in range2) or all(elem in range2 for elem in range1):
            total_encompasing_pairs += 1
        if any(elem in range1 for elem in range2) or any(elem in range2 for elem in range1):
            partial_encompasing_pairs += 1

    print("Ag*:", total_encompasing_pairs, answer_units,
          error_checker(total_encompasing_pairs, 2, 602))
    print("Au*:", partial_encompasing_pairs, answer_units,
          error_checker(partial_encompasing_pairs, 4, 891))


def day5():
    answer_units = "top boxes"
    silver_star_answer = cratemover9000()
    gold_star_answer = cratemover9001()
    print("Ag*:", silver_star_answer, answer_units,
          error_checker(silver_star_answer, "CMZ", "TWSGQHNHL"))
    print("Au*:", gold_star_answer, answer_units,
          error_checker(gold_star_answer, "MCD", "JNRSCDWPP"))


def cratemover9000():
    stax1, stax2, stax3, stax4, stax5, stax6, stax7, stax8, stax9, move_list = (
        pull_and_format_data())
    for move in move_list:
        how_many, from_stax, to_stax = parse_the_move_instructions(move_instruction=move)
        for num_times in range(how_many):
            leaving, arriving = translate_the_to_from_variables(
                stax1, stax2, stax3, stax4, stax5, stax6, stax7, stax8, stax9, from_stax,
                to_stax)
            arriving.appendleft(leaving.popleft())

    answer = format_the_answer(
        stax_list=[stax1, stax2, stax3, stax4, stax5, stax6, stax7, stax8, stax9])
    return answer


def cratemover9001():
    stax1, stax2, stax3, stax4, stax5, stax6, stax7, stax8, stax9, move_list = (
        pull_and_format_data())
    for move in move_list:
        how_many, from_stax, to_stax = parse_the_move_instructions(move_instruction=move)
        leaving, arriving = translate_the_to_from_variables(
            stax1, stax2, stax3, stax4, stax5, stax6, stax7, stax8, stax9, from_stax, to_stax)
        big_claw = []
        for num_times in range(how_many):
            take_off = leaving.popleft()
            big_claw.append(take_off)
        big_claw.reverse()
        for item in big_claw:
            arriving.appendleft(item)

    answer = format_the_answer(
        stax_list=[stax1, stax2, stax3, stax4, stax5, stax6, stax7, stax8, stax9])
    return answer


def pull_and_format_data():
    data_pack = import_data(day, dev_env, strip=False)
    stax1 = collections.deque()
    stax2 = collections.deque()
    stax3 = collections.deque()
    stax4 = collections.deque()
    stax5 = collections.deque()
    stax6 = collections.deque()
    stax7 = collections.deque()
    stax8 = collections.deque()
    stax9 = collections.deque()
    move_list = []

    for line in data_pack:
        if 'move' in line:
            move_list.append(line.strip())
        if "[" in line:
            if len(line) > 1 and line[1] != " ":
                stax1.append(line[1])
            if len(line) > 5 and line[5] != " ":
                stax2.append(line[5])
            if len(line) > 9 and line[9] != " ":
                stax3.append(line[9])
            if len(line) > 13 and line[13] != " ":
                stax4.append(line[13])
            if len(line) > 17 and line[17] != " ":
                stax5.append(line[17])
            if len(line) > 21 and line[21] != " ":
                stax6.append(line[21])
            if len(line) > 25 and line[25] != " ":
                stax7.append(line[25])
            if len(line) > 29 and line[29] != " ":
                stax8.append(line[29])
            if len(line) > 33 and line[33] != " ":
                stax9.append(line[33])

    return stax1, stax2, stax3, stax4, stax5, stax6, stax7, stax8, stax9, move_list


def format_the_answer(stax_list):
    answer = ""
    for item in stax_list:
        try:
            answer += item[0]
        except IndexError:
            pass
    return answer


def translate_the_to_from_variables(
        stax1, stax2, stax3, stax4, stax5, stax6, stax7, stax8, stax9, from_stax, to_stax):
    if from_stax == 1:
        leaving = stax1
    if to_stax == 1:
        arriving = stax1
    if from_stax == 2:
        leaving = stax2
    if to_stax == 2:
        arriving = stax2
    if from_stax == 3:
        leaving = stax3
    if to_stax == 3:
        arriving = stax3
    if from_stax == 4:
        leaving = stax4
    if to_stax == 4:
        arriving = stax4
    if from_stax == 5:
        leaving = stax5
    if to_stax == 5:
        arriving = stax5
    if from_stax == 6:
        leaving = stax6
    if to_stax == 6:
        arriving = stax6
    if from_stax == 7:
        leaving = stax7
    if to_stax == 7:
        arriving = stax7
    if from_stax == 8:
        leaving = stax8
    if to_stax == 8:
        arriving = stax8
    if from_stax == 9:
        leaving = stax9
    if to_stax == 9:
        arriving = stax9
    return leaving, arriving


def parse_the_move_instructions(move_instruction: str):
    moves = [int(s) for s in move_instruction.split() if s.isdigit()]
    how_many = moves[0]
    from_stax = moves[1]
    to_stax = moves[2]
    return how_many, from_stax, to_stax


def day6():
    data_pack = import_data(day, dev_env)
    answer_units = "location of start-of-packet marker"
    datastream_buffer = data_pack[0]
    silver_star_answer = find_the_starter(datastream_buffer, distinct_characters=4)
    gold_star_answer = find_the_starter(datastream_buffer, distinct_characters=14)
    print("Ag*:", silver_star_answer, answer_units,
          error_checker(silver_star_answer, 7, 1816))
    print("Au*:", gold_star_answer, answer_units,
          error_checker(gold_star_answer, 19, 2625))


def find_the_starter(datastream_buffer: str, distinct_characters: int):
    first_marker = distinct_characters - 1
    for ii in range(distinct_characters, len(datastream_buffer) + 1):
        first_marker += 1
        uniques = set(datastream_buffer[ii - distinct_characters:ii])
        if len(uniques) == distinct_characters:  # all are unique, no dupes
            return first_marker


def day7():
    # Thank you, anytree!
    data_pack = import_data(day, dev_env)
    answer_units = "total bytes in folder marked for deletion"
    at_most_this_big = 100000
    total_disk = 70000000
    required_for_update = 30000000
    root = Node("root", size=0)
    location_now = root
    nodes = dict()
    nodes[root.name] = root
    for jj in data_pack:
        if jj == "$ ls":
            # Do nothing. There are really only 5 conditions to handle, not 6.
            continue
        if "$ cd " in jj:  # This is ONLY for updating location_now.
            cd_where = jj.replace("$ cd ", "")
            if cd_where == "/":
                location_now = root
            elif cd_where == "..":
                location_now = location_now.parent
            else:
                unique_dict_key = get_unique_name(location_now=location_now, name=cd_where)
                location_now = nodes[unique_dict_key]
        else:  # This is ONLY for creating new nodes.
            first, name = jj.split(" ")
            if first == "dir":
                size = 0
            else:
                size = int(first)
            unique_dict_key = get_unique_name(location_now=location_now, name=name)
            node_count_before = len(nodes)
            nodes[unique_dict_key] = Node(name, parent=location_now, size=size)
            node_count_after = len(nodes)
            if node_count_before + 1 != node_count_after:
                # This held me up a long time.
                print(color_me("You got dupes!", "Red"), name, location_now, size)

    # for pre, fill, node in RenderTree(root):
    #    print("%s%s" % (pre, node.name), node.size)

    # Proud of this pretty picture:
    for pre, fill, node in RenderTree(root):
        if node.size:
            prefix = color_me("File:", "Magenta")
            display_size = f"\t{prefix} {node.size}"
        else:
            prefix = color_me("Dir:", "Cyan")
            dir_total = 0
            for child in node.descendants:
                dir_total += child.size
            display_size = f"\t{prefix} {dir_total}"
        print("%s%s" % (pre, node.name), display_size)
    print()

    total_smalls = 0
    folder_sizes = {}
    total_sizes_list = []
    for node in nodes:
        total_size = 0
        for child in nodes[node].descendants:
            total_size += child.size
        total_sizes_list.append(total_size)
        if total_size:
            folder_sizes[node] = total_size
        if total_size <= at_most_this_big:
            total_smalls += total_size

    print("Ag*:", total_smalls, answer_units, error_checker(total_smalls, 95437, 1667443))

    # print(folder_sizes)

    total_sizes_list.sort()
    largest_outside_dir = total_sizes_list[-1]
    unused_space = total_disk - largest_outside_dir
    space_needed = required_for_update - unused_space
    for one_size in total_sizes_list:
        if one_size > space_needed:
            print("Au*:", one_size, answer_units, error_checker(one_size, 24933642, 8998590))
            break


def get_unique_name(location_now: Node, name: str):
    unique_dict_key = ""
    for i in location_now.ancestors:
        unique_dict_key += i.name + "/"
    unique_dict_key += name + "/" + location_now.name
    return unique_dict_key


def day8():
    data_pack = import_data(day, dev_env)
    answer_units = "visible trees"
    grid = make_a_grid(data_pack)
    pp = pprint.PrettyPrinter(indent=4)
    grid = sweep_east(grid)
    grid = sweep_south(grid)
    grid = sweep_west(grid)
    grid = sweep_north(grid)
    # pp.pprint(grid)

    vt = score_it_up(grid)
    print("Ag*:", vt, answer_units, error_checker(vt, 21, 1798))

    grid = make_a_grid(data_pack)
    for line_index in range(len(grid)):
        for tree_index in range(len(grid[line_index])):
            tree_height = grid[line_index][tree_index][0]
            up = look_up(grid, tree_height, line_index, tree_index)
            down = look_down(grid, tree_height, line_index, tree_index)
            left = look_left(grid, tree_height, line_index, tree_index)
            right = look_right(grid, tree_height, line_index, tree_index)
            grid[line_index][tree_index] = [tree_height, up * down * left * right]

    # pp.pprint(grid)
    max_scenic_score = get_max_scenic_score(grid)
    print("Au*:", max_scenic_score, answer_units, error_checker(max_scenic_score, 8, 259308))


def make_a_grid(data_pack):
    grid = []
    for line in data_pack:
        treeline = []
        for char in line:
            one_tree = [int(char), 0]
            treeline.append(one_tree)
        grid.append(treeline)
    return grid


def sweep_east(grid):
    highest_so_far = 0
    for line_index in range(len(grid)):
        for tree_index in range(len(grid[line_index])):
            tree_height = grid[line_index][tree_index][0]
            if tree_index == 0 or tree_height > highest_so_far:
                highest_so_far = tree_height
                grid[line_index][tree_index] = [tree_height, 1]
    return grid


def sweep_south(grid):
    highest_so_far = 0
    for line_index in range(len(grid)):
        for tree_index in range(len(grid[line_index])):
            tree_height = grid[tree_index][line_index][0]
            if tree_index == 0 or tree_height > highest_so_far:
                highest_so_far = tree_height
                grid[tree_index][line_index] = [tree_height, 1]
    return grid


def sweep_west(grid):
    highest_so_far = 0
    for line_index in reversed(range(len(grid))):
        for tree_index in reversed(range(len(grid[line_index]))):
            tree_height = grid[line_index][tree_index][0]
            if tree_index == len(grid[0]) - 1 or tree_height > highest_so_far:
                highest_so_far = tree_height
                grid[line_index][tree_index] = [tree_height, 1]
    return grid


def sweep_north(grid):
    highest_so_far = 0
    for line_index in reversed(range(len(grid))):
        for tree_index in reversed(range(len(grid[line_index]))):
            tree_height = grid[tree_index][line_index][0]
            if tree_index == len(grid[0]) - 1 or tree_height > highest_so_far:
                highest_so_far = tree_height
                grid[tree_index][line_index] = [tree_height, 1]
    return grid


def score_it_up(grid):
    visible_trees = 0
    for line_index in range(len(grid)):
        for tree_index in range(len(grid[line_index])):
            visible_trees += grid[tree_index][line_index][1]
    return visible_trees


def look_right(grid, tree_height, x_coord, y_coord):
    # Return the number of trees one tree can see. Stop if you reach an edge
    # or at the first tree that is the same height or taller than the tree under consideration.
    right = 0
    for tree_index in range(y_coord + 1, len(grid[x_coord])):
        looking_at_height = grid[x_coord][tree_index][0]
        if tree_height > looking_at_height:
            right += 1
        elif tree_height <= looking_at_height:
            right += 1  # Count it and leave
            break
    return right


def look_up(grid, tree_height, x_coord, y_coord):
    up = 0
    for line_index in range(x_coord - 1, -1, -1):
        looking_at_height = grid[line_index][y_coord][0]
        if tree_height > looking_at_height:
            up += 1
        elif tree_height <= looking_at_height:
            up += 1  # Count it and leave
            break
    return up


def look_down(grid, tree_height, x_coord, y_coord):
    down = 0
    for line_index in range(x_coord + 1, len(grid)):
        looking_at_height = grid[line_index][y_coord][0]
        if tree_height > looking_at_height:
            down += 1
        elif tree_height <= looking_at_height:
            down += 1  # Count it and leave
            break
    return down


def look_left(grid, tree_height, x_coord, y_coord):
    left = 0
    for tree_index in range(y_coord - 1, -1, -1):
        looking_at_height = grid[x_coord][tree_index][0]
        if tree_height > looking_at_height:
            left += 1
        elif tree_height <= looking_at_height:
            left += 1  # Count it and leave
            break
    return left


def get_max_scenic_score(grid):
    max_scenic_score = 0
    for line_index in range(len(grid)):
        for tree_index in range(len(grid[line_index])):
            scenic_score = grid[tree_index][line_index][1]
            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score
    return max_scenic_score


def day9():
    data_pack = import_data(day, dev_env)
    answer_units = "spaces traveled by tail"

    h = [0, 0]
    t = [0, 0]
    t_occupied_spaces = set()

    # print(h, t)
    grid_vis(h, t)
    for move in data_pack:
        print("== ", move, " ==")
        h, t, t_occupied_spaces = perform_the_moves(
            h, t, direction=move[0], count=int(move[2]), t_occupied_spaces=t_occupied_spaces)

    print(t_occupied_spaces)
    grid_vis2(t_occupied_spaces)
    visited_spaces = len(t_occupied_spaces)
    print("Ag*:", visited_spaces, answer_units, error_checker(visited_spaces, 13, "higher"))
    # print("Au*:", answer, answer_units, error_checker(answer, dev_answer, prod_answer))


def perform_the_moves(h, t, direction, count, t_occupied_spaces):
    for ii in range(count):
        # Head moves first:
        h_x = h[0]
        h_y = h[1]
        if direction == "D":
            h_x -= 1  # D
        elif direction == "U":
            h_x += 1  # U
        elif direction == "L":
            h_y -= 1  # L
        elif direction == "R":
            h_y += 1  # R
        h = [h_x, h_y]

        # Tail moves second and obeys slightly different laws:
        t_x = t[0]
        t_y = t[1]
        # There are 8 possible movements when combo'd:
        if h_x - t_x > 1:
            t_x += 1  # U
            if h_y > t_y:
                t_y += 1  # R
            if h_y < t_y:
                t_y -= 1  # L
        elif t_x - h_x > 1:
            t_x -= 1  # D
            if h_y > t_y:
                t_y += 1  # R
            if h_y < t_y:
                t_y -= 1  # L
        elif h_y - t_y > 1:
            t_y += 1  # R
            if h_x > t_x:
                t_x += 1  # U
            if h_x < t_x:
                t_x -= 1  # D
        elif t_y - h_y > 1:
            t_y -= 1  # L
            if h_x > t_x:
                t_x += 1  # U
            if h_x < t_x:
                t_x -= 1  # D

        t_occupied_spaces.add(f"{t[0]} {t[1]}")
        t = [t_x, t_y]
        grid_vis(h, t)
    return h, t, t_occupied_spaces


def grid_vis(h, t):
    global dev_env
    if not dev_env:
        return
    grid = []
    for i in range(5):
        interior_grid = []
        for jj in range(6):
            if i == 4 - h[0] and jj == h[1]:
                interior_grid.append("H")
            elif i == 4 - t[0] and jj == t[1]:
                interior_grid.append("T")
            elif i == 4 and jj == 0:
                interior_grid.append("s")
            else:
                interior_grid.append(".")
        grid.append([interior_grid])
    for line in grid:
        for chars in line:
            print("".join(chars))
    print()


def grid_vis2(t_occupied_spaces):
    score = 0
    global dev_env
    if not dev_env:
        grid_vis3(t_occupied_spaces)
    grid = []
    for i in range(5):
        interior_grid = []
        for jj in range(6):
            # for item in t_occupied_spaces:
            if i == 4 and jj == 0:
                interior_grid.append("s")
            elif f"{4 - i} {jj}" in t_occupied_spaces:
                interior_grid.append("#")
            else:
                interior_grid.append(".")
        grid.append([interior_grid])
    for line in grid:
        for chars in line:
            print("".join(chars))
            for each in chars:
                if each != ".":
                    score += 1
    print(score)
    return grid, score


def grid_vis3(t_occupied_spaces):
    xgrid = 300
    ygrid = 200
    # zero_spot = int(grid_size / 2)
    score = 0
    grid = []
    for i in range(xgrid):
        interior_grid = []
        for jj in range(ygrid):
            if i == 150 and jj == 120:
                interior_grid.append("s")
            elif f"{150 - i} {120 - jj}" in t_occupied_spaces:
                interior_grid.append("#")
            else:
                interior_grid.append(".")
        grid.append([interior_grid])
    for line in grid:
        for chars in line:
            print("".join(chars))
            for each in chars:
                if each != ".":
                    score += 1
    print(score)
    return grid, score


# run_all_days(8)
run_one_day(9, include_prod=True)
