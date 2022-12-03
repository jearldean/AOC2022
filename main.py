def execute():
    globals()[f"day{day}"]()


def import_data(day: int, dev_env: bool = True):
    folder = 'DEV' if dev_env else "PROD"
    data_path = f"{folder}/{day}.txt"
    data_pack = []
    f = open(data_path)
    for line in f:
        data_pack.append(line.strip())
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


day = 3
dev_env = False

execute()
