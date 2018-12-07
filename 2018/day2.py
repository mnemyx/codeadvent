INPUT_DATA = 'day2_input.txt'
sample_data = ['abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxyz']

def read_input_data(infile=INPUT_DATA): 
    with open(infile, 'r') as f: 
        data = [x.strip() for x in f.readlines()]
    return data 

def get_counts(in_data, checksum_only=True):
    counts = {2: 0, 3: 0}
    for line in in_data:
        for i in (2, 3):
            if [x for x in line if line.count(x) == i]:
                counts[i] += 1
    if checksum_only:
        return counts[2] * counts[3]
    return counts

def find_similar_ids(in_data, common_only=True):
    def is_diff_by_one(str1, str2):
        results = []
        for i in range(len(str1)):
            results.append(str1[i] == str2[i])
        return results.count(False) == 1, results

    for s1 in in_data[:-1]:
        for s2 in in_data[1:]:
            is_diff, diff_res = is_diff_by_one(s1, s2)
            if is_diff and common_only:
                return [s1[i] for i in range(len(s1)) if diff_res[i] is True]
            elif is_diff and not common_only:
                return s1, s2

in_data = read_input_data()

checksum = get_counts(in_data)
print("Part 1:", checksum)

common_letters = find_similar_ids(in_data)
print("Part 2:", ''.join(common_letters))