from commonlib import determine_day, read_input_data


DAY = determine_day(__file__)
SAMPLE_DATA = [1, -2, 3, +1]


def read_func(f):
    return [int(x.strip()) for x in f.readlines()]


def find_final_freq(in_data):
    final = 0
    for x in in_data:
        final += x
    return final


def find_dup_freq(in_data): 
    final = 0 
    frequencies = []
    while True: 
        for x in in_data: 
            if final in frequencies: 
                return final 
            frequencies.append(final) 
            final += x


def exec_day(sample=False):
    if sample:
        in_data = SAMPLE_DATA
    else:
        in_data = read_input_data(DAY, read_func)

    final_freq = find_final_freq(in_data)
    print("Part 1:", final_freq)

    dup_freq = find_dup_freq(in_data)
    print("Part 2:", dup_freq)