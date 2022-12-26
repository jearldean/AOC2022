import collections
from anytree import Node, RenderTree
import pprint
from functools import reduce
import operator
from collections import defaultdict
import doctest
import math
import ast
import matplotlib.pyplot as plt

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


def original_day9_not_working():
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


def day10():
    data_pack = import_data(day, dev_env)
    answer_units = "total signal strengths"
    cycles_to_record = [20, 60, 100, 140, 180, 220]
    signal_strengths = []
    x = 1
    cycles = 0
    for instruction in data_pack:
        if instruction == 'noop':
            cycles += 1
            if cycles in cycles_to_record:
                signal_strengths.append(x)
        else:
            cycles += 1
            if cycles in cycles_to_record:
                signal_strengths.append(x)
            cycles += 1
            if cycles in cycles_to_record:
                signal_strengths.append(x)
            x += int(instruction.replace("addx ", ""))

    answer = 0
    for zz in range(len(cycles_to_record)):
        answer += cycles_to_record[zz] * signal_strengths[zz]
    print("Ag*:", answer, answer_units, error_checker(answer, 13140, 14240))

    # Part 2:
    my_answer2 = "\n"
    cycle = 0
    x = 1
    sprite = [x - 1, x, x + 1]

    for instruction in data_pack:
        if instruction == 'noop':
            if cycle in sprite:
                my_answer2 += "#"
            else:
                my_answer2 += "."
            # print(cycle, ":", x, sprite, my_answer2)
            cycle += 1
            if cycle == 40:
                my_answer2 += "\n"
                cycle = 0
        else:
            if cycle in sprite:
                my_answer2 += "#"
            else:
                my_answer2 += "."
            cycle += 1
            # print(cycle, ":", x, sprite, my_answer2)
            if cycle == 40:
                my_answer2 += "\n"
                cycle = 0

            if cycle in sprite:
                my_answer2 += "#"
            else:
                my_answer2 += "."
            cycle += 1
            # print(cycle, ":", x, sprite, my_answer2)
            if cycle == 40:
                my_answer2 += "\n"
                cycle = 0
            x += int(instruction.replace("addx ", ""))
            sprite = [x - 1, x, x + 1]  # This is the only time we update the sprite location.

    dev_answer2 = "\n##..##..##..##..##..##..##..##..##..##.." \
                  "\n###...###...###...###...###...###...###." \
                  "\n####....####....####....####....####...." \
                  "\n#####.....#####.....#####.....#####....." \
                  "\n######......######......######......####" \
                  "\n#######.......#######.......#######.....\n"
    prod_answer = "\n###..#....#..#.#....#..#.###..####.#..#." \
                  "\n#..#.#....#..#.#....#.#..#..#....#.#..#." \
                  "\n#..#.#....#..#.#....##...###....#..####." \
                  "\n###..#....#..#.#....#.#..#..#..#...#..#." \
                  "\n#....#....#..#.#....#.#..#..#.#....#..#." \
                  "\n#....####..##..####.#..#.###..####.#..#.\n"
    answer_units = "buncha 2's, buncha 3's, buncha 4's..." if dev_env else "PLULKBZH"
    print("Au*:", my_answer2, answer_units, error_checker(my_answer2, dev_answer2, prod_answer))


def day11():
    data_pack = import_data(day, dev_env)
    answer_units = "monkey inspections"
    monkey_data = monkey_parser(data_pack)
    answer = do_many_rounds(rounds=20, relief_divisor=3, monkey_data=monkey_data)
    print("Ag*:", answer, answer_units, error_checker(answer, 10605, 101436))

    monkey_data = monkey_parser(data_pack)  # Fresh Data Pack
    answer = do_many_rounds(rounds=10000, relief_divisor=1, monkey_data=monkey_data)
    print("Au*:", answer, answer_units, error_checker(answer, 2713310158, 19754471646))


def do_many_rounds(rounds, relief_divisor, monkey_data):
    monkey_inspections = []
    for monkey in range(len(monkey_data)):
        monkey_inspections.append(0)

    for ee in range(rounds):
        monkey_data, monkey_inspections = do_one_round(
            monkey_data, monkey_inspections, relief_divisor)

    """
        if ee in [0, 19, 999, 2999, 3999, 4999, 5999, 6999, 7999, 8999, 9999]:
            print(f"== After round {ee + 1} ==")
            print(monkey_inspections)

    for monkey_dict in monkey_data:
        item_list = monkey_dict["Items"]
        monkey_number = monkey_dict["Monkey"]
        print(f"Monkey {monkey_number}: {item_list}")
    """

    monkey_inspections.sort(reverse=True)
    answer = monkey_inspections[0] * monkey_inspections[1]
    # print(monkey_inspections, monkey_inspections[0], "*", monkey_inspections[1], "=", answer)
    return answer


def do_one_round(monkey_data, monkey_inspections, relief_divisor):
    """
    Monkey 1:
        Monkey inspects an item with a worry level of 54.
            Worry level increases by 6 to 60.
            Monkey gets bored with item. Worry level is divided by 3 to 20.
            Current worry level is not divisible by 19.
            Item with worry level 20 is thrown to monkey 0.
    """
    for monkey in range(len(monkey_data)):
        # print(f"Monkey {monkey}:")
        for item in reversed(monkey_data[monkey]["Items"]):
            monkey_inspections[monkey] += 1
            # print("monkey_inspections", monkey_inspections)
            # print(f"\tMonkey inspects an item with a worry level of {item}.")
            new_worry_level = monkey_operation(
                item, monkey_data[monkey]["Operation"])  # new = old * 19
            if relief_divisor != 1:
                new_worry_level /= relief_divisor
            new_worry_level = int(new_worry_level)
            # print(f"\t\tMonkey gets bored with item.
            # Worry level is divided by 3 to {new_worry_level}.")
            test_divisor = monkey_data[monkey]["Test"]
            if is_it_divisible(new_worry_level, test_divisor):
                # print(f"\t\tCurrent worry level is divisible by {test_divisor}.")
                throw_item(monkey_data, from_monkey=monkey,
                           to_monkey=monkey_data[monkey]["True"],
                           worry_level_of_item=new_worry_level, old_worry_level=item)
            else:
                # print(f"\t\tCurrent worry level is not divisible by {test_divisor}.")
                throw_item(monkey_data, from_monkey=monkey,
                           to_monkey=monkey_data[monkey]["False"],
                           worry_level_of_item=new_worry_level, old_worry_level=item)
    return monkey_data, monkey_inspections


def monkey_operation(old, operation):
    last_word = operation.split(" ")[-1]
    if last_word == "old":  # square
        new = old * old
        # print(f"\t\tWorry level is multiplied by itself to {new}.")
        return new
    elif "+" in operation:
        new = old + int(last_word)
        # print(f"\t\tWorry level increases by {int(last_word)} to {new}.")
        return new
    elif "*" in operation:
        new = old * int(last_word)
        # print(f"\t\tWorry level is multiplied by {int(last_word)} to {new}.")
        return new


def throw_item(monkey_data, from_monkey, to_monkey, worry_level_of_item, old_worry_level):
    old_items = monkey_data[from_monkey]["Items"]
    old_items.remove(old_worry_level)
    monkey_data[from_monkey]["Items"] = old_items

    old_items = monkey_data[to_monkey]["Items"]
    # old_items.append(worry_level_of_item)  # Not good enough for Part 2.

    """Got a tip from mjpieters - really had no idea how to bring it down from exponential runtime.
    "Luckily, we can cap the worry levels to the product of all the monkeys' divisible values;
    e.g. the example monkeys have divisible test values 17, 13, 19 and 23, so worry levels
    can be reduced by taking their modulo with 96577:"""
    lcm = reduce(operator.mul, (monkey["Test"] for monkey in monkey_data))

    old_items.append(worry_level_of_item % lcm)
    monkey_data[to_monkey]["Items"] = old_items

    # print(f"\t\tItem with worry level {worry_level_of_item} is thrown to monkey {to_monkey}.")
    return monkey_data


def monkey_parser(data_pack):
    """
    Monkey 0:
    Starting items: 79, 98
    Operation: new = old * 19
    Test: divisible by 23
        If true: throw to monkey 2
        If false: throw to monkey 3

    """
    monkey_counter = 0
    monkey_data = []
    one_monkeys_data = {}
    for dd in data_pack:
        if not dd:
            monkey_data.append(one_monkeys_data)
            monkey_counter += 1
            one_monkeys_data = {}  # Reset this
        else:
            if "Monkey" in dd:  # Monkey 0:
                one_monkeys_data["Monkey"] = int(dd.replace("Monkey ", "").replace(":", ""))
            elif "Starting" in dd:  # Starting items: 79, 98
                items_list_str = dd.replace("Starting items: ", "")
                items_list = items_list_str.split(", ")
                real_items_list = []
                for item in items_list:
                    real_items_list.append(int(item))
                one_monkeys_data["Items"] = real_items_list
            elif "Operation" in dd:  # Operation: new = old * 19
                one_monkeys_data["Operation"] = dd.replace("Operation: ", "")
            elif "Test: divisible by" in dd:  # Test: divisible by 23
                one_monkeys_data["Test"] = int(dd.replace("Test: divisible by ", ""))
            elif "true" in dd:  # If true: throw to monkey 2
                one_monkeys_data["True"] = int(dd.replace("If true: throw to monkey ", ""))
            elif "false" in dd:  # If false: throw to monkey 3
                one_monkeys_data["False"] = int(dd.replace("If false: throw to monkey ", ""))

    monkey_data.append(one_monkeys_data)
    # print(monkey_data)
    return monkey_data


def is_it_divisible(a_number, evenly_divisible_by):
    if a_number % evenly_divisible_by == 0:
        return True
    else:
        return False


def day9():
    """
    Taking another stab at Day 9.
    Got a hint from mjpieters:
    "The first thing to realise is that, if the tail moves, it'll move to the location the head was
    just at."
    Nope, I did something else before.

    "So how to know when to move the tail?
    Calculate the maximum distance in either direction between tail and head after moving the head;
    if it is greater than 1, move the tail to where the head just was."
    Yes, I was doing that.
    """
    data_pack = import_data(day, dev_env)
    answer_units = "spaces traveled by tail"

    visited_spaces = perform_the_moves_9(data_pack)
    print("Ag*:", visited_spaces, answer_units, error_checker(visited_spaces, 13, 6642))
    visited_spaces = perform_the_moves_9(data_pack, knots=10)  # 5339 was too high
    print("Au*:", visited_spaces, answer_units, error_checker(visited_spaces, 1, 6642))


def perform_the_moves_9(data_pack, knots=2):
    current_configuration = []
    for ii in range(knots):
        current_configuration.append([0, 0])
    t_occupied_spaces = set()
    t_occupied_spaces.add("[0, 0]")
    for move in data_pack:
        current_configuration, t_occupied_spaces = pull_the_string(
            move, current_configuration, t_occupied_spaces)
    visited_spaces = len(t_occupied_spaces)
    return visited_spaces


def pull_the_string(move, current_configuration, t_occupied_spaces):
    direction = move.split(" ")[0]
    num_moves = int(move.split(" ")[1])
    for dd in range(num_moves):
        new_configuration = []
        for knot in range(len(current_configuration)):
            if knot == 0:  # Head
                new_node = move_the_head(
                    direction=direction, current_configuration=current_configuration)
            else:  # Followers are 1-9
                new_node = move_the_tail(leader=new_configuration[knot - 1],
                                         follower=current_configuration[knot],
                                         leaders_last_position=current_configuration[knot - 1])
            new_configuration.append(new_node)
        t_occupied_spaces.add(f"[{new_configuration[-1][0]}, {new_configuration[-1][1]}]")
        current_configuration = new_configuration
        print(current_configuration)
    return current_configuration, t_occupied_spaces


def one_click(current_configuration, direction, last_positions):
    interim_data = []
    for knot in range(len(current_configuration)):
        if knot == 0:  # Head
            new_node = move_the_head(
                direction=direction, current_configuration=current_configuration)
        else:  # Followers are 1-9
            new_node = move_the_tail(leader=current_configuration[knot - 1],
                                     follower=current_configuration[knot],
                                     leaders_last_position=last_positions[knot - 1])
        interim_data.append(new_node)
    return interim_data


def move_the_head(direction, current_configuration):
    hx = current_configuration[0][0]
    hy = current_configuration[0][1]
    if direction == "D":
        hx -= 1
    elif direction == "U":
        hx += 1
    elif direction == "L":
        hy -= 1
    elif direction == "R":
        hy += 1
    return [hx, hy]


def move_the_tail(leader, follower, leaders_last_position):
    if leader in wheres_my_9(follower):
        return follower  # No move.
    else:  # Now T will occupy the last space held by H
        return leaders_last_position


def wheres_my_9(a_coordinate):
    # What are the 9 surrounding and inclusive coordinates of a single coordinate?
    x = a_coordinate[0]
    y = a_coordinate[1]
    return [[x, y], [x + 1, y], [x, y + 1], [x - 1, y], [x, y - 1],
            [x + 1, y + 1], [x - 1, y - 1], [x + 1, y - 1], [x - 1, y + 1]]


def day12():
    graph = Graph()
    data_pack = import_data(day, dev_env)
    answer_units = "steps"
    grid = []
    for row in data_pack:
        line = []
        for char in row:
            line.append(char)
        grid.append(line)

    begin = None
    end = None
    for vertical in range(len(grid)):
        for horizontal in range(len(grid[vertical])):
            char = grid[vertical][horizontal]
            coordinate_name = f'{vertical} {horizontal}'
            neighbors = get_my_neighbors(grid, vertical, horizontal, v_bound=len(grid),
                                         h_bound=len(grid[vertical]))
            for neighbor in neighbors:  # [{f'{vertical-1} {horizontal}': neighbor_char}, ]
                for neighbor_coordinate_name in neighbor:
                    neighbor_char = neighbor[neighbor_coordinate_name]
                    cost = work_out_the_cost(char, neighbor_char)
                    if cost == 0:  # Don't add forbidden paths to the possible solution.
                        graph.add_edge(coordinate_name, neighbor_coordinate_name, cost)
                        print(f"{char}:{coordinate_name}\t"
                              f"{neighbor_char}:{neighbor_coordinate_name}\tcost={cost}")
                    if neighbor_char == "S":
                        begin = neighbor_coordinate_name
                    if neighbor_char == "E":
                        end = neighbor_coordinate_name

    out = dijsktra(graph, begin, end)
    print(out, len(out))
    # goals = [s_vert, s_horiz, e_vert, e_horiz]

    # answer = find_shortest_path(grid, goals)
    print("Ag*:", len(out), answer_units, error_checker(len(out), 31, 0))
    # print("Au*:", answer, answer_units, error_checker(answer, 0, 0))


def work_out_the_cost(char1, char2):
    if char1 in ["S", "E"]:
        if char1 == "S":
            cost1 = 0
        if char1 == "E":
            cost1 = 27
    else:
        cost1 = ord(char1) - 96
    if char2 in ["S", "E"]:
        if char2 == "S":
            cost2 = 0
        if char2 == "E":
            cost2 = 27
    else:
        cost2 = ord(char2) - 96
    if cost2 > cost1 and abs(cost2 - cost1) <= 1:
        cost = 0
    else:
        cost = 10
    return cost


def get_my_neighbors(grid, vertical, horizontal, v_bound, h_bound):
    neighbors = []
    if vertical < v_bound - 1:
        neighbor_char = grid[vertical + 1][horizontal]
        neighbors.append({f'{vertical + 1} {horizontal}': neighbor_char})
    if vertical > 0:
        neighbor_char = grid[vertical - 1][horizontal]
        neighbors.append({f'{vertical - 1} {horizontal}': neighbor_char})
    if horizontal < h_bound - 1:
        neighbor_char = grid[vertical][horizontal + 1]
        neighbors.append({f'{vertical} {horizontal + 1}': neighbor_char})
    if horizontal > 0:
        neighbor_char = grid[vertical][horizontal - 1]
        neighbors.append({f'{vertical} {horizontal - 1}': neighbor_char})
    return neighbors


def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if
                             node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path


class Graph():
    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight


def day20212():
    # Wanted to take an alternate look at last year's Day 2
    data_pack = import_data(day, dev_env)
    answer_units = "position product"

    x_position = 0
    y_position = 0
    for instruction in data_pack:
        instruction_pieces = instruction.split(" ")
        direction = instruction_pieces[0]
        number = int(instruction_pieces[1])
        if direction == "forward":
            x_position += number
        elif direction == "down":
            y_position += number
        elif direction == "up":
            y_position -= number
    answer = y_position * x_position
    print("Ag*:", answer, answer_units, error_checker(answer, 150, 2039912))

    # Or another way:
    forwards = 0
    downs = 0
    ups = 0
    for instruction in data_pack:
        instruction_pieces = instruction.split(" ")
        direction = instruction_pieces[0]
        number = int(instruction_pieces[1])
        if direction == "forward":
            forwards += number
        elif direction == "down":
            downs += number
        elif direction == "up":
            ups += number
    answer = forwards * (downs - ups)
    print("Ag*:", answer, answer_units, error_checker(answer, 150, 2039912))

    """How does AIM change things?
    down X increases your aim by X units.
    up X decreases your aim by X units.
    forward X does two things:
    It increases your horizontal position by X units.
    It increases your depth by your aim multiplied by X."""
    x_position = 0
    y_position = 0
    aim = 0
    for instruction in data_pack:
        instruction_pieces = instruction.split(" ")
        direction = instruction_pieces[0]
        number = int(instruction_pieces[1])
        if direction == "forward":
            x_position += number
            y_position += number * aim
        elif direction == "down":
            aim += number
        elif direction == "up":
            aim -= number
    answer = y_position * x_position
    print("Au*:", answer, answer_units, error_checker(answer, 900, 1942068080))


def day13():
    data_pack = import_data(day, dev_env)
    answer_units = "sum of indices in the right order"
    transformed_data = transform_data(data_pack)
    print(transformed_data)

    right_order_pairs = 0
    for index in range(len(transformed_data)):
        if compare_o(transformed_data[index]):  # are balanced, bool
            print(f"Pair {index + 1}: {transformed_data[index]} are in the right order.")
            right_order_pairs += index + 1
        print()

    print("Ag*:", right_order_pairs, answer_units, error_checker(right_order_pairs, 13, "?"))
    # print("Au*:", right_order_pairs, answer_units, error_checker(right_order_pairs, 150, 2039912))


def transform_data(data_pack):
    transformed_data = []
    pairs = []
    for line in data_pack:
        if line:
            line = ast.literal_eval(line)  # Oh shit, this worked a damn dreaam!
            pairs.append(line)
        else:
            transformed_data.append(pairs)
            pairs = []
    transformed_data.append(pairs)
    return transformed_data


def compare_o(compare_these_pairs):
    """
    If both values are integers, the lower integer should come first.
    If the left integer is lower than the right integer, the inputs are in the right order.
    If the left integer is higher than the right integer, the inputs are not in the right order.
    Otherwise, the inputs are the same integer; continue checking the next part of the input.

    If both values are lists, compare the first value of each list, then the second value, and so on
    If the left list runs out of items first, the inputs are in the right order.
    If the right list runs out of items first, the inputs are not in the right order.
    If the lists are the same length and no comparison makes a decision about the order,
    continue checking the next part of the input.

    If exactly one value is an integer, convert the integer to a list which contains that integer
    as its only value, then retry the comparison.
    For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2);
    the result is then found by instead comparing [0,0,0] and [2].
    """
    left_thing, right_thing = compare_these_pairs
    print(f'IN: Comparing {left_thing} and {right_thing}')
    most_members = max(len(left_thing), len(right_thing))
    for ii in range(most_members):
        try:
            print(f"len iter = {ii}: left_thing={left_thing[ii]}, right_thing={right_thing[ii]}")
            if isinstance(left_thing[ii], int) and isinstance(right_thing[ii], int):
                if left_thing[ii] > right_thing[ii]:
                    print(
                        f"OUT: {left_thing[ii]}>{right_thing[ii]}, so inputs are not in the right order")
                    return False
                elif left_thing[ii] < right_thing[ii]:
                    print(
                        f"OUT: {left_thing[ii]}<{right_thing[ii]}, so inputs are in the right order")
                    return True
                # else:
                #    return compare_o(compare_these_pairs=compare_these_pairs)
            elif isinstance(left_thing[ii], list) and isinstance(right_thing[ii], list):
                print("DOWN: Both lists; Diving in one level")
                return compare_o(compare_these_pairs=[left_thing[ii], right_thing[ii]])
            elif isinstance(left_thing[ii], int) and isinstance(right_thing[ii], list):
                print(f"DOWN: Transform {left_thing[ii]} into [{left_thing[ii]}]; recompare.")
                return compare_o(compare_these_pairs=[[left_thing[ii]], right_thing[ii]])
            elif isinstance(left_thing[ii], list) and isinstance(right_thing[ii], int):
                print(f"DOWN: Transform {right_thing[ii]} into [{right_thing[ii]}]; recompare.")
                return compare_o(compare_these_pairs=[left_thing[ii], [right_thing[ii]]])
        except IndexError:  # Right side ran out of items, so inputs are not in the right order
            if len(left_thing) > len(right_thing):
                print("OUT: Right side ran out of items, so inputs are not in the right order")
                return False
            elif len(left_thing) < len(right_thing):
                print("OUT: Left side ran out of items, so inputs are in the right order")
                return True


def compare_o2(compare_these_pairs):
    left_thing, right_thing = compare_these_pairs
    # print(f'IN: Comparing {left_thing} and {right_thing}')
    most_members = max(len(left_thing), len(right_thing))
    # for ii in range(most_members):
    try:
        print(f"left_thing={left_thing[0]}, right_thing={right_thing[0]}")
    except IndexError:
        print("Oops")


def day14():
    data_pack = import_data(day, dev_env)
    answer_units = "sand grains"
    answer = 0
    print("Ag*:", answer, answer_units, error_checker(answer, 24, 6642))
    print("Au*:", answer, answer_units, error_checker(answer, 1, 6642))


def day15():
    data_pack = import_data(day, dev_env)
    answer_units = "positions that cannot host a beacon"

    new_data = fix_day_15_data(data_pack)
    # print(new_data)

    if dev_env:
        important_row = 10
        skew = important_row + 2
    else:
        important_row = 2000000
        skew = important_row + 10000
    # plot_the_data(new_data)  # That was fun to learn, not sure it's helpful yet.
    """Pseudocode:
    1. plot the data
    2. get the DISTANCE to each B from S (pythagorean theorem? Nope.)
    3. Change the plot to BLOT OUT every spot within those radii.
    """
    all_xs = []
    all_ys = []
    for one_coordinate in new_data:
        all_xs.append(one_coordinate[0][0])
        all_xs.append(one_coordinate[1][0])
        all_ys.append(one_coordinate[0][1])
        all_ys.append(one_coordinate[1][1])
    max_x = max(all_xs) + 10 + skew
    max_y = max(all_ys) + 10 + skew

    plotter = []
    for y in range(max_y):
        a_line = []
        for x in range(max_x):
            a_line.append(".")
        plotter.append(a_line)

    for one_coordinate in new_data:
        plotter = make_a_square_around_me(plotter, one_coordinate, skew)

    answer = 0
    string = ""
    for row in plotter:
        string += row[important_row + skew]
        if row[important_row + skew] == "#":
            answer += 1
    print(string)
    print("Ag*:", answer, answer_units, error_checker(answer, 26, 6642))
    # print("Au*:", answer, answer_units, error_checker(answer, 1, 6642))


def make_a_square_around_me(plotter, one_coordinate, skew):
    s = one_coordinate[0]
    b = one_coordinate[1]
    dist = one_coordinate[2]
    # Find the radius number:
    radius = abs(dist[0]) + abs(dist[1])

    # print(one_coordinate, radius)
    for expando in range(radius + 1):
        retracto = radius - expando
        for sy in range(s[1] - retracto + skew, s[1] + retracto + skew + 1):
            for sx in range(s[0] - expando + skew, s[0] + expando + skew + 1):
                if plotter[sx][sy] not in ["S", "B"]:
                    plotter[sx][sy] = "#"
    plotter[s[0] + skew][s[1] + skew] = "S"
    plotter[b[0] + skew][b[1] + skew] = "B"
    # for a in plotter:
    #    print("".join(a))
    # print()
    return plotter


def plot_the_data(new_data):
    for coords in new_data:
        plt.plot(coords[0][0], coords[0][1], 'bs')
        plt.plot(coords[1][0], coords[1][1], 'rs')
    plt.axis([-2, 25, 25, -2])
    plt.show()


def fix_day_15_data(data_pack):
    # Sensor at x=2, y=18: closest beacon is at x=-2, y=15
    new_data = []
    for line in data_pack:
        pieces = line.split(" ")
        sx = int(pieces[2].replace("x=", "").replace(",", ""))
        sy = int(pieces[3].replace("y=", "").replace(":", ""))
        bx = int(pieces[8].replace("x=", "").replace(",", ""))
        by = int(pieces[9].replace("y=", ""))
        # distance = math.sqrt(abs(sx-bx)*abs(sx-bx) + abs(sy-by)*abs(sy-by))
        new_data.append([[sx, sy], [bx, by], [bx - sx, by - sy]])
    return new_data


def day16():
    data_pack = import_data(day, dev_env)
    answer_units = "pressure released"

    open_a_valve = 1  # min
    follow_a_tunnel = 1  # min
    time_remaining = 30  # min
    time_elapsed = 0  # min
    open_valves = []
    pressure_released = 0
    new_data = fix_data_pack(data_pack)
    print(new_data)

    print("Ag*:", pressure_released, answer_units, error_checker(pressure_released, 1651, 6642))
    # print("Au*:", answer, answer_units, error_checker(answer, 1, 6642))


def do_the_routine(new_data, time_remaining, open_a_valve=1, follow_a_tunnel=1):
    flo = 0
    for jj in time_remaining:
        decide_what_to_do()


def decide_what_to_do():
    move_to_a_valve()


def fix_data_pack(data_pack, include_zeros=False):
    # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    new_data = []
    for a_string in data_pack:
        one_valve = []
        words = a_string.split(" ")
        one_valve.append(words[1])
        flow = int(words[4].replace(";", "").replace("rate=", ""))
        one_valve.append(flow)
        gates = []
        for route in words[9:]:
            gates.append(route)
        one_valve.append(gates)
        if flow == 0 and not include_zeros:
            continue
        new_data.append(one_valve)
    return new_data


def costs_a_minute(time_remaining, time_elapsed):
    time_remaining -= 1
    time_elapsed += 1
    return time_remaining, time_elapsed


def open_a_valve(time_remaining, time_elapsed):
    time_remaining, time_elapsed = costs_a_minute(time_remaining, time_elapsed)


def move_to_a_valve(time_remaining, time_elapsed):
    time_remaining, time_elapsed = costs_a_minute(time_remaining, time_elapsed)


def day17():
    data_pack = import_data(day, dev_env)
    answer_units = "rock height"
    answer = 0
    print("Ag*:", answer, answer_units, error_checker(answer, 3068, 6642))
    # print("Au*:", answer, answer_units, error_checker(answer, 1, 6642))


def day18():
    data_pack = import_data(day, dev_env)
    answer_units = "surface area"
    surf = 0
    print("Ag*:", surf, answer_units, error_checker(surf, 64, 6642))
    # print("Au*:", answer, answer_units, error_checker(answer, 1, 6642))


def day19():
    data_pack = import_data(day, dev_env)
    answer_units = "Total Quality Levels"

    minutes = 24
    robot_prices = fix_data_pack_19(data_pack)
    for blueprint in robot_prices:
        for min_ in range(minutes):
            robot_prices = run_one_day19(robot_prices, blueprint, min_ + 1)

    print(robot_prices)
    ans = quality_level_and_answer(robot_prices)
    print("Ag*:", ans, answer_units, error_checker(ans, 33, 6642))
    # print("Au*:", answer, answer_units, error_checker(answer, 1, 6642))


def run_one_day19(robot_prices, blueprint, minute):
    """Each robot can collect 1 of its resource type per minute.

    It also takes one minute for the robot factory (also conveniently from your pack)
    to construct any type of robot, although it consumes the necessary resources available
    when construction begins."""
    print(f"== Minute {minute} ==")
    buying_a_robot = None

    # Buy a robot.
    for robot in ['geode', 'obsidian', 'clay', 'ore']:  # Try to buy the biggest you can first
        ore_i_have = robot_prices[blueprint]['ore'][2]
        clay_i_have = robot_prices[blueprint]['clay'][2]
        obsidian_i_have = robot_prices[blueprint]['obsidian'][2]

        robot_price, robot_count, rock_count = robot_prices[blueprint][robot]
        enough_ore = robot_price[0] <= ore_i_have
        enough_clay = robot_price[1] <= clay_i_have
        enough_obsidian = robot_price[2] <= obsidian_i_have
        if enough_ore and enough_clay and enough_obsidian:
            # Delete the payment
            buying_a_robot = robot
            new_ore_count = ore_i_have - robot_price[0]
            new_clay_count = clay_i_have - robot_price[1]
            new_obsidian_count = obsidian_i_have - robot_price[2]
            robot_price, robot_count, rock_count = robot_prices[blueprint]['ore']
            robot_prices[blueprint]['ore'] = [robot_price, robot_count, new_ore_count]
            robot_price, robot_count, rock_count = robot_prices[blueprint]['clay']
            robot_prices[blueprint]['clay'] = [robot_price, robot_count, new_clay_count]
            robot_price, robot_count, rock_count = robot_prices[blueprint]['obsidian']
            robot_prices[blueprint]['obsidian'] = [robot_price, robot_count, new_obsidian_count]
            print(f"Spend {robot_prices[blueprint][robot][0]} on a {buying_a_robot}.")
            break
        # robot_prices[blueprint][robot] = [robot_price, robot_count, rock_count]

    # mine:
    for robot in ['geode', 'obsidian', 'clay', 'ore']:
        robot_price, robot_count, rock_count = robot_prices[blueprint][robot]
        rock_count += robot_count * 1
        robot_prices[blueprint][robot] = [robot_price, robot_count, rock_count]
        print(f"{robot} mined, now have {rock_count}.")

    # collect new robot
    if buying_a_robot:
        robot_price, robot_count, rock_count = robot_prices[blueprint][buying_a_robot]
        robot_prices[blueprint][buying_a_robot] = [robot_price, robot_count + 1, rock_count]
        print(f"{buying_a_robot} robot is delivered. Now have {robot_count + 1}.")
    print()
    return robot_prices


def fix_data_pack_19(data_pack):
    """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot
    costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian."""
    fixed_data_pack = {}
    for line in data_pack:
        words = line.split(" ")
        blueprint = int(words[1].replace(":", ""))
        ore_robot_price = [int(words[6]), 0, 0]
        clay_robot_price = [int(words[12]), 0, 0]
        obsidian_robot_price = [int(words[18]), int(words[21]), 0]
        geode_robot_price = [int(words[27]), 0, int(words[30])]
        fixed_data_pack[blueprint] = {'ore': [ore_robot_price, 1, 0],
                                      'clay': [clay_robot_price, 0, 0],
                                      'obsidian': [obsidian_robot_price, 0, 0],
                                      'geode': [geode_robot_price, 0, 0]}
    return fixed_data_pack


def quality_level_and_answer(robot_prices):
    """
    Determine the quality level of each blueprint by multiplying that blueprint's ID number with the
    largest number of geodes that can be opened in 24 minutes using that blueprint. In this example,
    the first blueprint has ID 1 and can open 9 geodes, so its quality level is 9. The second
    blueprint has ID 2 and can open 12 geodes, so its quality level is 24. Finally, if you add up
    the quality levels of all of the blueprints in the list, you get 33.
    :return:
    """
    running_total = 0
    for key in robot_prices:
        running_total += key * robot_prices[key]['geode'][2]
    return running_total


def day20():
    # Wow, yeah. My solution is really inefficient. A circular list would've solved this in no time.
    # This took about AN HOUR to run but got the right answer!
    data_pack = import_data(day, dev_env)
    answer_units = "sum of grove coordinates"

    for mix in range(10):
        mixed = mix_20(data_pack)

    grove_coordinates = 0
    for dd in [1, 2, 3]:
        grove_coordinate = count_it_20(mixed, number_after_0=(dd * 1000))
        # print(grove_coordinate)
        grove_coordinates += grove_coordinate

    # print("Ag*:", grove_coordinates, answer_units, error_checker(grove_coordinates, 3, 6642))
    print("Au*:", grove_coordinates, answer_units,
          error_checker(grove_coordinates, 1623178306, 6642))


def count_it_20(mixed, number_after_0):
    length = len(mixed)
    index_0 = 0
    for zz in range(length):
        if mixed[zz] == 0:
            index_0 = zz
    move_this_many = number_after_0 % length
    if move_this_many < length - index_0:
        return mixed[index_0 + move_this_many]
    else:
        return mixed[index_0 - length + move_this_many]


def mix_20(data_pack):
    """The encrypted file is a list of numbers. To mix the file, move each number forward or
    backward in the file a number of positions equal to the value of the number being moved.
    The list is circular, so moving a number off one end of the list wraps back around to the other
    end as if the ends were connected.

    For example, to move the 1 in a sequence like 4, 5, 6, 1, 7, 8, 9, the 1 moves one position
    forward: 4, 5, 6, 7, 1, 8, 9. To move the -2 in a sequence like 4, -2, 5, 6, 7, 8, 9, the -2
    moves two positions backward, wrapping around: 4, 5, 6, 7, 8, -2, 9.

    The numbers should be moved in the order they originally appear in the encrypted file.
    Numbers moving around during the mixing process do not change the order in which the
    numbers are moved."""
    decryption_key = 811589153
    i_index_list = []
    length = len(data_pack)
    for ii in range(length):
        i_index_list.append(
            [ii, int(data_pack[ii] * decryption_key), ii])  # [original_index, value, index_now]

    for _ in range(10):  # This is so going to croak.
        for gg in range(length):
            # Let's just make references to the indices change and leave the overall order the same.
            i_index_list = move_it(i_index_list, length, this_index=gg)
            print(i_index_list)  # , "\t", mixed)

    mixed = order_it(i_index_list)
    return mixed


def order_it(i_index_list):
    mixed = []
    for jj in range(len(i_index_list)):
        for each_list in i_index_list:
            if each_list[2] == jj:
                mixed.append(each_list[1])
                break
    return mixed


def move_it(i_index_list, length, this_index):
    _, value, leaving_index = i_index_list[this_index]
    if value == 0:
        # print(f"{value} does not move:")
        return i_index_list  # No change.
    new_index = (value + leaving_index) % (length - 1)
    if new_index == 0:  # Just fix this to match the example. Others used a circular list.
        new_index = length - 1
    # print(f"{value} moves from {leaving_index} to new index {new_index}:")
    for nn in range(length):  # 0 thru 6...
        old_index = i_index_list[nn][2]
        if this_index == nn:
            # print(f"I '{i_index_list[nn][1]}' am landing on index {new_index}")
            i_index_list[this_index][2] = new_index
        elif leaving_index < old_index <= new_index:  # landed on you.
            # print(f"Shove down the '{i_index_list[nn][1]}' to index {old_index - 1}")
            i_index_list[nn][2] = old_index - 1
        elif new_index <= old_index <= leaving_index:  # landed on you.
            # print(f"Push up the '{i_index_list[nn][1]}' to index {old_index + 1}")
            i_index_list[nn][2] = old_index + 1
        else:
            # print(f"'{i_index_list[nn][1]}' does not move.")
            pass
    # print(i_index_list)
    return i_index_list


def day21():
    data_pack = import_data(day, dev_env)
    day21a(data_pack)
    day21b(data_pack)


def day21_process_monkey_data(data_pack):
    monkeys = {}
    for line in data_pack:
        pieces = line.split(": ")
        try:
            monkeys[pieces[0]] = int(pieces[1])
        except:
            monkeys[pieces[0]] = pieces[1]
    return monkeys


def day21a(data_pack):
    answer_units = "Number yelled by monkey"
    monkeys = day21_process_monkey_data(data_pack)
    monkeys = day21a_solver(monkeys)
    answer = int(monkeys['root'])
    print("Ag*:", answer, answer_units, error_checker(answer, 152, 85616733059734))


def day21a_solver(monkeys):
    while isinstance(monkeys['root'], str):
        for key in monkeys:
            if isinstance(monkeys[key], str):
                monkey_pieces = monkeys[key].split(" ")
                a = monkey_pieces[0]
                oper = monkey_pieces[1]
                b = monkey_pieces[2]
                if isinstance(monkeys[a], (int, float)) and isinstance(monkeys[b], (int, float)):
                    monkeys[key] = eval(f"{monkeys[a]}{oper}{monkeys[b]}")
    return monkeys


def day21b(data_pack, humn_guess=0):
    answer_units = "Number yelled by human"
    monkeys = day21_process_monkey_data(data_pack)
    monkeys['humn'] = humn_guess
    new_condition = monkeys['root'].replace("+", "-")
    monkeys['root'] = new_condition
    monkeys = day21a_solver(monkeys)
    if abs(monkeys['root']) < 0.1:
        good_enough = round(humn_guess)
        print("Au*:", good_enough, answer_units, error_checker(good_enough, 301, 3560324848168))
    else:
        diff = monkeys['root']
        if dev_env:
            new_humn_guess = humn_guess - diff
            # print(diff, new_humn_guess)
            day21b(data_pack, humn_guess=new_humn_guess)  # Oops, recursion!
        else:
            new_humn_guess = humn_guess + (diff * .01)  # Need a different guesser, I guess.
            # print(diff, new_humn_guess)
            day21b(data_pack, humn_guess=new_humn_guess)  # Oops, recursion!


def day22():
    data_pack = import_data(day, dev_env)
    answer_units = "sum of"
    answer = 0

    final_row = 6
    final_column = 8
    final_facing = 0
    final_password = 1000 * final_row + final_column * 4 + final_facing

    print("Ag*:", final_password, answer_units, error_checker(final_password, 6032, 6642))
    # print("Au*:", answer, answer_units, error_checker(answer, 1, 6642))


def day23():
    data_pack = import_data(day, dev_env)
    answer_units = "empty ground tiles"

    """Simulate the Elves' process and find the smallest rectangle that contains the Elves after 
    10 rounds. How many empty ground tiles does that rectangle contain?
    """
    rounds = 30
    coords = format_the_data_23(data_pack)  # {elf_number: [x_coordinate, y_coordinate]}
    elf_count = len(coords)
    empty_tiles = 0
    tapped_out_after = 0
    round = 0
    # for round in range(rounds):
    while tapped_out_after == 0:
        # print("Start Round", round)
        # print_a_picture(coords)
        coords, proposals = first_move(coords, round)
        # print(coords)
        # print(proposals)
        if not proposals:
            tapped_out_after = round + 1
            break
        coords = second_move(coords, proposals)
        # print_a_picture(coords)
        if round == 10:
            empty_tiles = find_grid_area(coords) - elf_count  # Total area - occupied squares
        round += 1

    print("Ag*:", empty_tiles, answer_units, error_checker(empty_tiles, 110, 4068))
    print("Au*:", tapped_out_after, "rounds until tapped out",
          error_checker(tapped_out_after, 20, 100))


def print_a_picture(coords):
    grid = 20
    printy_grid = []
    for ii in range(grid):
        inside = []
        for jj in range(grid):
            inside.append(". ")
        printy_grid.append(inside)
    for elf in coords:
        x, y = coords[elf]
        printy_grid[y + 6][x + 6] = str(elf) if elf > 9 else f"{elf} "
    for line in printy_grid:
        print("".join(line))


def format_the_data_23(data_pack):
    coords = dict()
    elf_count = 0
    for y_coord in range(len(data_pack)):
        for x_coord in range(len(data_pack[y_coord])):
            # print(data_pack[y_coord], data_pack[y_coord][x_coord], y_coord, x_coord)
            if data_pack[y_coord][x_coord] == "#":
                elf_count += 1
                coords[elf_count] = [x_coord, y_coord]
    return coords


def find_my_8(my_coords):
    """Find the 8 squares around you."""
    x, y = my_coords
    my_8 = [[x - 1, y - 1], [x, y - 1], [x + 1, y - 1],
            [x - 1, y], [x + 1, y],
            [x - 1, y + 1], [x, y + 1], [x + 1, y + 1]]
    return my_8


def count_find_uniques(coordo_dict):
    # When counts are more than 1, you got collisions.
    space_counts = dict()
    for elf in coordo_dict:
        space_counts[coordo_dict[elf]] = space_counts.get(coordo_dict[elf], 0) + 1
    return space_counts


def first_move(coords, round):
    """During the first half of each round, each Elf considers the eight positions adjacent to
    themself. If no other Elves are in one of those eight positions, the Elf does not do anything
    during this round. Otherwise, the Elf looks in each of four directions in the following order
    and proposes moving one step in the first valid direction:

    If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
    If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
    If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
    If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.


    my_8 = [[x - 1, y - 1], [x, y - 1], [x + 1, y - 1],
            [x - 1, y],                     [x + 1, y],
            [x - 1, y + 1], [x, y + 1], [x + 1, y + 1]]

    Finally, at the end of the round, the first direction the Elves considered is moved to the
    end of the list of directions. For example, during the second round, the Elves would try
    proposing a move to the south first, then west, then east, then north. On the third round,
    the Elves would first consider west, then east, then north, then south
    """
    # print("round=", round)
    proposals = dict()
    all_coordinates = list(coords.values())
    for elf in coords:
        # If no other Elves are in one of those eight positions, the Elf does not do anything during this round.
        nearby_elves = [coo for coo in find_my_8(coords[elf]) if coo in all_coordinates]
        # print(elf, nearby_elves)
        if nearby_elves:
            x, y = coords[elf]
            north_places = [[x - 1, y - 1], [x, y - 1], [x + 1, y - 1]]
            south_places = [[x - 1, y + 1], [x, y + 1], [x + 1, y + 1]]
            west_places = [[x - 1, y - 1], [x - 1, y], [x - 1, y + 1]]
            east_places = [[x + 1, y - 1], [x + 1, y], [x + 1, y + 1]]
            rotato = {0: north_places,
                      1: south_places,
                      2: west_places,
                      3: east_places}
            # for dd in range(4):
            #    print((round + dd) % 4)
            if not [coo for coo in rotato[(round + 0) % 4] if coo in all_coordinates]:
                proposals[elf] = rotato[(round + 0) % 4][1]  # Middle item of _places
                continue
            if not [coo for coo in rotato[(round + 1) % 4] if coo in all_coordinates]:
                proposals[elf] = rotato[(round + 1) % 4][1]
                continue
            if not [coo for coo in rotato[(round + 2) % 4] if coo in all_coordinates]:
                proposals[elf] = rotato[(round + 2) % 4][1]
                continue
            if not [coo for coo in rotato[(round + 3) % 4] if coo in all_coordinates]:
                proposals[elf] = rotato[(round + 3) % 4][1]
                continue
    # print()
    return coords, proposals


def second_move(coords, proposals):
    """After each Elf has had a chance to propose a move, the second half of the round can begin.
    Simultaneously, each Elf moves to their proposed destination tile if they were the only Elf to
    propose moving to that position. If two or more Elves propose moving to the same position,
    none of those Elves move.

    # space_counts = count_find_uniques(proposals)

        #if space_counts[proposals[elf]] == 1:  # and proposals.get(
        # elf) is not None:  # If 2 or more, the elf does not move.
        #if not [coo for coo in proposals[elf] if coo in ]:
    """
    for elf in proposals:  # if no collision, them move there.
        collision = False
        for all_other_elves in coords:
            if all_other_elves != elf and proposals.get(all_other_elves) == proposals[elf]:
                collision = True
        if not collision:
            coords[elf] = proposals[elf]
    return coords


def find_grid_area(coords):
    """To make sure they're on the right track, the Elves like to check after round 10 that they're
    making good progress toward covering enough ground. To do this, count the number of empty
    ground tiles contained by the smallest rectangle that contains every Elf."""
    coords.values()
    x_es = [g[0] for g in coords.values()]
    y_s = [g[1] for g in coords.values()]
    x_axis = (max(x_es) - min(x_es)) + 1
    y_axis = (max(y_s) - min(y_s)) + 1
    return x_axis * y_axis


def day24():
    data_pack = import_data(day, dev_env)
    answer_units = "blizzard moves"
    answer = 0

    print("Ag*:", answer, answer_units, error_checker(answer, 18, "?"))
    print("Au*:", answer, "rounds until tapped out", error_checker(answer, "?", "?"))


def day25():
    data_pack = import_data(day, dev_env)
    answer_units = "SNAFU number"
    doctest.testmod()
    decimals = []
    for ii in data_pack:
        decimal = convert_from_snafu(snafu=ii)
        decimals.append(decimal)
    snafu = convert_to_snafu(decimal=sum(decimals))
    print("Ag*:", snafu, answer_units, error_checker(snafu, '2=-1=0', "2-==10===-12=2-1=-=0"))


def convert_from_snafu(snafu):
    """
    Say you have the SNAFU number 2=01.
    That's 2 in the 625s place, = (double-minus) in the 125s place, - (minus) in the 25s place,
    0 in the 5s place, and 1 in the 1s place.
    (2 times 625) plus (-2 times 125) plus (-1 times 25) plus (0 times 5) plus (1 times 1).
    That's 1250 plus -250 plus -25 plus 0 plus 1. 976!

    >>> convert_from_snafu("20")
    10
    >>> convert_from_snafu("2=-01")
    976
    >>> convert_from_snafu("1=-0-2")
    1747
    >>> convert_from_snafu("12111")
    906
    >>> convert_from_snafu("2=0=")
    198
    >>> convert_from_snafu("21")
    11
    >>> convert_from_snafu("2=01")
    201
    >>> convert_from_snafu("111")
    31
    >>> convert_from_snafu("20012")
    1257
    >>> convert_from_snafu("112")
    32
    >>> convert_from_snafu("1=-1=")
    353
    >>> convert_from_snafu("1-12")
    107
    >>> convert_from_snafu("12")
    7
    >>> convert_from_snafu("1=")
    3
    >>> convert_from_snafu("122")
    37
    """
    decimal = 0
    places = len(snafu)
    for index in range(places):
        multi = 5 ** (places - index - 1)
        resident = snafu[index]
        try:
            decimal += int(resident) * multi
        except ValueError:
            if resident == "=":
                decimal += multi * -2
            elif resident == "-":
                decimal += multi * -1
    return decimal


def convert_to_snafu(decimal):
    """
    You know how starting on the right, normal numbers have a ones place, a tens place, a hundreds
    place, and so on, where the digit in each place tells you how many of that value you have?"

    SNAFU works the same way, except it uses powers of five instead of ten.
    Starting from the right, you have a ones place, a fives place, a twenty-fives place,
    a one-hundred-and-twenty-fives place, and so on. It's that easy!"

    You ask why some of the digits look like - or = instead of "digits".
    You know, I never did ask the engineers why they did that.
    Instead of using digits four through zero, the digits are 2, 1, 0, minus (written -),
    and double-minus (written =). Minus is worth -1, and double-minus is worth -2."

    So, because ten (in normal numbers) is two fives and no ones, in SNAFU it is written 20.
    Since eight (in normal numbers) is two fives minus two ones, it is written 2=."

    >>> convert_to_snafu(4890)
    '2=-1=0'
    >>> convert_to_snafu(1747)
    '1=-0-2'
    >>> convert_to_snafu(906)
    '12111'
    >>> convert_to_snafu(198)
    '2=0='
    >>> convert_to_snafu(11)
    '21'
    >>> convert_to_snafu(201)
    '2=01'
    >>> convert_to_snafu(31)
    '111'
    >>> convert_to_snafu(1257)
    '20012'
    >>> convert_to_snafu(32)
    '112'
    >>> convert_to_snafu(353)
    '1=-1='
    >>> convert_to_snafu(107)
    '1-12'
    >>> convert_to_snafu(7)
    '12'
    >>> convert_to_snafu(3)
    '1='
    >>> convert_to_snafu(37)
    '122'
    """
    snafu = ""
    while decimal > 0:
        # Had to look at https://carbon.now.sh/?bg=rgba%28171%2C+184%2C+195%2C+1%29&t=seti&wt=none&l=python&width=680&ds=true&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Hack&fs=14px&lh=133%25&si=false&es=2x&wm=false&code=from%2520functools%2520import%2520reduce%250A%250Adef%2520SNAFUtoDec%28num%29%253A%250A%2520%2520%2520%2520return%2520reduce%28%250A%2520%2520%2520%2520%2520%2520%2520%2520lambda%2520r%252C%2520v%253A%2520%28%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520r%255B0%255D%2520%252B%2520%28%2522%253D-012%2522.index%28v%29%2520-%25202%29*%2520r%255B1%255D%252C%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520r%255B1%255D%2520*%25205%252C%250A%2520%2520%2520%2520%2520%2520%2520%2520%29%252C%250A%2520%2520%2520%2520%2520%2520%2520%2520num%255B%253A%253A-1%255D%252C%250A%2520%2520%2520%2520%2520%2520%2520%2520%280%252C%25201%29%252C%250A%2520%2520%2520%2520%29%255B0%255D%250A%250Adef%2520DecToSNAFU%28num%29%253A%2520%2523%2520assume%2520non-zero%250A%2520%2520%2520%2520res%2520%253D%2520%255B%255D%250A%2520%2520%2520%2520while%2520num%2520%253E%25200%253A%250A%2520%2520%2520%2520%2520%2520%2520%2520res.append%28%2522012%253D-%2522%255Bnum%2520%2525%25205%255D%29%250A%2520%2520%2520%2520%2520%2520%2520%2520num%2520%253D%2520%282%2520%252B%2520num%29%2520%252F%252F%25205%250A%2520%2520%2520%2520return%2520%27%27.join%28res%255B%253A%253A-1%255D%29%250A%250Aprint%2520%28DecToSNAFU%28sum%28SNAFUtoDec%28l%29%2520for%2520l%2520in%2520open%280%29.read%28%29.splitlines%28%29%29%29%29
        snafu += "012=-"[decimal % 5]
        # so, dec = 3:  "012=-"[3] == '=', corresponds to -2    5-2=3   so, = in the ones place.
        decimal = (2 + decimal) // 5
        # the floor division // rounds the result down to the nearest whole number:
        # 3+2 = 5    and  5//5=1   so, go around again with decimal=1
    return snafu[::-1]  # Print it backwards ('=1' that we assembled becomes '1=')


# run_all_days(11)
run_one_day(25, include_prod=True)
