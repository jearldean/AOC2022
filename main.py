import collections
from anytree import Node, RenderTree


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


def day1():
    data_pack = import_data(day, dev_env)
    elf_stores = []
    running_total = 0

    for food_unit in data_pack:
        if not food_unit:
            elf_stores.append(running_total)
            running_total = 0
        else:
            running_total += int(food_unit)

    elf_stores.sort(reverse=True)
    print(elf_stores[0])
    print(elf_stores[0] + elf_stores[1] + elf_stores[2])


def day2():
    # https://adventofcode.com/2022/day/2
    data_pack = import_data(day, dev_env)
    overall_score1 = 0
    overall_score2 = 0
    for i in data_pack:
        first, second = i.split(" ")
        overall_score1 += rock_paper_scissors1(hers=first, mine=second)
        overall_score2 += rock_paper_scissors2(hers=first, outcome_code=second)
    print(overall_score1)
    print(overall_score2)


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
    sum_the_priorities = 0
    for rucksack in data_pack:
        pouch_item_count = int(len(rucksack) / 2)
        dupe_item = find_the_dupe_item([rucksack[:pouch_item_count], rucksack[pouch_item_count:]])
        if dupe_item:
            sum_the_priorities += get_priority(char=dupe_item)
    print("Ag:", sum_the_priorities)

    sum_the_priorities = 0
    for elf_group_number in range(1, int((len(data_pack) / 3) + 1)):
        elf_group_set = elf_group_number * 3
        elf_group_packs = [data_pack[elf_group_set - 3], data_pack[elf_group_set - 2],
                           data_pack[elf_group_set - 1]]
        dupe_item = find_the_dupe_item(elf_group_packs)
        sum_the_priorities += get_priority(char=dupe_item)
    print("Au:", sum_the_priorities)


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
    print("Ag:", total_encompasing_pairs)
    print("Au:", partial_encompasing_pairs)


def day5():
    cratemover9000()
    cratemover9001()


def cratemover9000():
    stax1, stax2, stax3, stax4, stax5, stax6, stax7, stax8, stax9, move_list = (
        pull_and_format_data())
    for move in move_list:
        how_many, from_stax, to_stax = parse_the_move_instructions(move_instruction=move)
        for num_times in range(how_many):
            leaving, arriving = translate_the_to_from_variables(
                stax1, stax2, stax3, stax4, stax5, stax6, stax7, stax8, stax9, from_stax, to_stax)
            arriving.appendleft(leaving.popleft())

    answer = format_the_answer(
        stax_list=[stax1, stax2, stax3, stax4, stax5, stax6, stax7, stax8, stax9])
    print("Ag:", answer)


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
    print("Au:", answer)


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
    datastream_buffer = data_pack[0]
    print("Ag:", find_the_starter(datastream_buffer, distinct_characters=4))
    print("Au:", find_the_starter(datastream_buffer, distinct_characters=14))


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
                unique_dict_key = cd_where + str(location_now)
                location_now = nodes[unique_dict_key]
        else:  # This is ONLY for creating new nodes.
            first, name = jj.split(" ")
            if first == "dir":
                size = 0
            else:
                size = int(first)
            unique_dict_key = name + str(location_now)
            node_count_before = len(nodes)
            nodes[unique_dict_key] = Node(name, parent=location_now, size=size)
            node_count_after = len(nodes)
            if node_count_before + 1 != node_count_after:
                # This held me up a long time.
                print("You got dupes!", name, location_now, size)

    # Proud of this pretty picture:
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name), node.size)

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
    # print(folder_sizes)
    print("Ag:", total_smalls)

    total_sizes_list.sort()
    largest_outside_dir = total_sizes_list[-1]
    unused_space = total_disk - largest_outside_dir
    space_needed = required_for_update - unused_space
    for one_size in total_sizes_list:
        if one_size > space_needed:
            print("Au:", one_size)
            break


day = 7
dev_env = False

execute()
