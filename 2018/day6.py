from collections import namedtuple, defaultdict

from commonlib import determine_day, read_input_data


DAY = determine_day(__file__)
SAMPLE_DATA = [
    '1, 1',
    '1, 6',
    '8, 3',
    '3, 4',
    '5, 5',
    '8, 9',
    '7, 2',
]


Coords = namedtuple('Coords', ['x', 'y'])


def convert_to_coords(in_data, delim=","):
    coordinates = []
    for line in in_data:
        points = [int(p.strip()) for p in line.split(delim)]
        coordinates.append(Coords(x=points[0], y=points[1]))
    return coordinates


def calc_manhattan_dist(c1, c2):
    return abs(c1.x - c2.x) + abs(c1.y - c2.y)


def find_min_max(coords):
    p_x = [c.x for c in coords]
    p_y = [c.y for c in coords]
    return min(p_x), max(p_x), min(p_y), max(p_y)


def map_and_calc_areas(coords):
    # Find min/max x, y coordinates
    min_x, max_x, min_y, max_y = find_min_max(coords)
    cached = dict()
    mapped = defaultdict(list)
    infinites = set()
    for coord in coords:
        if coord.x in (min_x, max_x) or coord.y in (min_y, max_y):
            infinites.add(coord)
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if (x, y) in cached:
                    tmp = cached[(x, y)]
                else:
                    tmp = Coords(x=x, y=y)
                man_dist = calc_manhattan_dist(tmp, coord)
                mapped[tmp].append((coord, man_dist))

    areas = defaultdict(int)
    for m, data in mapped.items():
        sorted_data = sorted(data, key=lambda x: x[1])
        # Coordinates with infinite areas aren't always
        # the ones with min/max x, y coordinates. They're
        # also any coordinates whose area range manage to 
        # reach said min/max with the shortest distance.
        if m.x in (min_x, max_x) or m.y in (min_y, max_y):
            infinites.add(sorted_data[0][0])
        if [d for c, d in sorted_data].count(sorted_data[0][1]) == 1:
            areas[sorted_data[0][0]] += 1
    return mapped, areas, infinites


def find_largest_area(areas, infinites=(), exclude_infinites=True):
    areas_sorted = []
    for c, a in sorted(areas.items(), key=lambda kv: kv[1], reverse=True): 
        if exclude_infinites and c in infinites:
            continue
        areas_sorted.append((c, a))
    return areas_sorted[0]


def find_most_nearby_coords(mapped, max_dist_sum=10000):
    acceptable = list()
    for m, data in mapped.items():
        if sum([d for c, d in data]) < max_dist_sum:
            acceptable.append(m)
    return acceptable


def exec_day(sample=False):
    if sample:
        in_data = SAMPLE_DATA
    else:
        in_data = read_input_data(DAY)

    coords = convert_to_coords(in_data)
    mapped, areas, infinites = map_and_calc_areas(coords)

    p1 = find_largest_area(areas, infinites)
    print("Part 1:", p1[0], p1[1])

    p2 = find_most_nearby_coords(mapped)
    print("Part 2:", len(p2))
