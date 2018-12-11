import re
from datetime import datetime, timedelta
from collections import namedtuple, defaultdict, Counter

INPUT_DATA = 'day4_input.txt'
unsorted_sample_data = [
    '[1518-11-05 00:45] falls asleep',
    '[1518-11-03 00:29] wakes up',
    '[1518-11-01 00:00] Guard #10 begins shift',
    '[1518-11-04 00:02] Guard #99 begins shift',
    '[1518-11-01 00:05] falls asleep',
    '[1518-11-01 00:25] wakes up',
    '[1518-11-05 00:55] wakes up',
    '[1518-11-01 00:55] wakes up',
    '[1518-11-01 23:58] Guard #99 begins shift',
    '[1518-11-02 00:40] falls asleep',
    '[1518-11-02 00:50] wakes up',
    '[1518-11-03 00:24] falls asleep',
    '[1518-11-01 00:30] falls asleep',
    '[1518-11-04 00:36] falls asleep',
    '[1518-11-04 00:46] wakes up',
    '[1518-11-05 00:03] Guard #99 begins shift',
    '[1518-11-03 00:05] Guard #10 begins shift',
]

sorted_sample_data = [
    '[1518-11-01 00:00] Guard #10 begins shift',
    '[1518-11-01 00:05] falls asleep',
    '[1518-11-01 00:25] wakes up',
    '[1518-11-01 00:30] falls asleep',
    '[1518-11-01 00:55] wakes up',
    '[1518-11-01 23:58] Guard #99 begins shift',
    '[1518-11-02 00:40] falls asleep',
    '[1518-11-02 00:50] wakes up',
    '[1518-11-03 00:05] Guard #10 begins shift',
    '[1518-11-03 00:24] falls asleep',
    '[1518-11-03 00:29] wakes up',
    '[1518-11-04 00:02] Guard #99 begins shift',
    '[1518-11-04 00:36] falls asleep',
    '[1518-11-04 00:46] wakes up',
    '[1518-11-05 00:03] Guard #99 begins shift',
    '[1518-11-05 00:45] falls asleep',
    '[1518-11-05 00:55] wakes up'
]


Entry = namedtuple('Entry', ['timestamp', 'message'])


def read_input_data(infile=INPUT_DATA): 
    with open(infile, 'r') as f: 
        data = [x.strip() for x in f.readlines()]
    return data 

def convert_input(in_data, do_sort=True):
    regex = re.compile(r"\[(?P<ts>[\d\-\:\s]+)\]\s(?P<msg>.+)")
    ts_format = "%Y-%m-%d %H:%M"
    entries = []
    for line_no, x in enumerate(in_data):
        res = regex.match(x)
        if not res:
            print("Error parsing line {0}: '{1}'".format(line_no, x))
            continue
        ts = datetime.strptime(res['ts'], ts_format)
        entries.append(Entry(timestamp=ts, message=res['msg']))
    if do_sort:
        return sorted(entries, key=lambda entry: entry.timestamp)
    return entries 


def parse_guard_naps(entries):
    nap = dict()
    curr_id = None
    guards = defaultdict(dict)
    re_guard = re.compile(r"Guard\s#(?P<id>\d+).+")
    
    for entry in entries:
        res = re_guard.match(entry.message)
        if res:
            curr_id = res['id']

            if entry.timestamp.hour != 00:
                # This honor roll guard started his shift early
                ts = entry.timestamp.date() + timedelta(days=1)
            else:
                ts = entry.timestamp.date()

            guards[curr_id][ts] = list()
            nap = dict()
        else:
            if entry.message == "falls asleep":
                nap['start'] = entry.timestamp.minute
            elif entry.message == "wakes up":
                nap['end'] = entry.timestamp.minute
                # Naps entries appear to always start during 
                # hour 00 and never ends during or after hour 01
                guards[curr_id][entry.timestamp.date()].append(nap)
                nap = dict()
    return guards


def compile_guard_nap_minutes(gnaps, results_only=True):
    nap_lengths = defaultdict(list)
    for guard, nap_data in gnaps.items():
        for day, naps in nap_data.items():
            for nap in naps:
                nap_lengths[guard].extend(range(nap['start'], nap['end']))
    return nap_lengths


def find_max_sleepiest(naps):
    sleepiest = None
    max_nappage = []
    for guard, nap in naps.items():
        if len(nap) > len(max_nappage):
            max_nappage = nap
            sleepiest = int(guard)
    nap_min = Counter(max_nappage).most_common(1)[0][0]
    return sleepiest, nap_min, sleepiest * nap_min


def find_mode_sleepiest(naps):
    sleepiest_modes = list()
    for guard, nap in naps.items():
        if nap:
            modes = Counter(nap).most_common()
            cnt = modes[0][1]
            for nmin, ncnt in modes:
                if ncnt != cnt:
                    continue
                sleepiest_modes.append((int(guard), nmin, ncnt))
    sm = sorted(sleepiest_modes, key=lambda n: n[2])[-1]
    return sm[0], sm[1], sm[0] * sm[1]


in_data = read_input_data()
entries = convert_input(in_data)
#print("Sorting Test:", convert_input(sorted_sample_data, False) == entries)

gnaps = parse_guard_naps(entries)
naps = compile_guard_nap_minutes(gnaps)
p1 = find_max_sleepiest(naps)
print("Part 1: {0} * {1} = {2}".format(*p1))

p2 = find_mode_sleepiest(naps)
print("Part 2: {0} * {1} = {2}".format(*p2))

