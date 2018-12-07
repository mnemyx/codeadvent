INPUT_DATA = 'day1_input.txt'
DEBUG = False

def read_input_data(infile=INPUT_DATA): 
    with open(infile, 'r') as f: 
        data = [int(x.strip()) for x in f.readlines()]
    return data 

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
        if DEBUG:
            print("...no duplicate frequencies encountered; restarting...")


in_data = read_input_data()

final_freq = find_final_freq(in_data)
print("Part 1:", final_freq)

dup_freq = find_dup_freq(in_data)
print("Part 2:", dup_freq)