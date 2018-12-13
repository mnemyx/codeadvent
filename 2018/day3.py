import re
from collections import namedtuple

from commonlib import determine_day, read_input_data


DAY = determine_day(__file__)
SAMPLE_DATA = ['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2', '#4 @ 5,5: 2x2', '#5 @ 3,3: 2x2', '#6 @ 7,1: 4x4']

Claim = namedtuple('Claim', ['claim_id', 'min_x', 'min_y', 'max_x', 'max_y'])


def parse_into_bboxes(in_data):
    regex = re.compile(r"#(?P<claim>\d+)\s?@\s?(?P<min_x>\d+),(?P<min_y>\d+):\s(?P<width>\d+)x(?P<height>\d+)")
    claims = []
    for x in in_data:
        res = regex.match(x)
        if not res:
            print("Error parsing line: '{0}'".format(x))
            continue
        claims.append(Claim(claim_id=res['claim'], 
                            min_x=int(res['min_x']), 
                            min_y=int(res['min_y']),
                            max_x=int(res['min_x']) + int(res['width']),
                            max_y=int(res['min_y']) + int(res['height'])))
    return claims


def iter_claims(claims):
    for indx, claim1 in enumerate(claims[:-1], 1):
        for claim2 in claims[indx:]:
            yield claim1, claim2


def determine_min_max(c1, c2, axis="x"):
    if axis == "x":
        max_attr = 3
        min_attr = 1
    else:
        max_attr = 4
        min_attr = 2
    claim1 = (c1[min_attr], c1[max_attr])
    claim2 = (c2[min_attr], c2[max_attr])
    if (claim2[0] <= claim1[0] <= claim2[1] or 
        claim2[0] <= claim1[1] <= claim2[1]) or \
            (claim1[0] <= claim2[0] <= claim1[1] or 
             claim1[0] <= claim2[1] <= claim1[1]):
        min_val = max(claim1[0], claim2[0])
        max_val = min(claim1[1], claim2[1])
        return min_val, max_val


def find_overlapping(claims, total_only=True, claims_only=False):
    overlapped = set()
    overlapped_claims = set()
    for claim1, claim2 in iter_claims(claims):
        # Find X-overlap
        x = determine_min_max(claim1, claim2, axis="x")
        # Find Y-overlap
        y = determine_min_max(claim1, claim2, axis="y")
        if None not in (x, y):
            overlapped_claims.add(claim1)
            overlapped_claims.add(claim2)
            for i in range(x[0], x[1]):
                for j in range(y[0], y[1]):
                    overlapped.add((i, j))
    if claims_only:
        return overlapped_claims
    if total_only:
        return len(overlapped)        
    return overlapped


def find_no_overlap(claims):
    overlapped = find_overlapping(claims, False, True)
    return set(claims).difference(overlapped)


def exec_day(sample=False):
    if sample:
        in_data = SAMPLE_DATA
    else:
        in_data = read_input_data(DAY)

    claims = parse_into_bboxes(in_data)

    overlapped = find_overlapping(claims)
    print("Part 1:", overlapped)

    good_claim = find_no_overlap(claims)
    print("Part 2:", good_claim)

