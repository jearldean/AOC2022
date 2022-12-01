def import_data(day: int, dev_env: bool = True):
    folder = 'DEV' if dev_env else "PROD"
    data_path = f"{folder}/{day}.txt"
    data_pack = []
    f = open(data_path)
    for line in f:
        data_pack.append(line.strip())
    return data_pack


def day1():
    # data_pack = import_data(1)
    data_pack = import_data(1, False)
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


day1()
