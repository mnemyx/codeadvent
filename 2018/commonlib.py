import os


def determine_day(mod_path):
    return os.path.splitext(os.path.basename(mod_path))[0].replace('day', '')


def read_input_data(day, call_func=None):
    indir = os.path.dirname(os.path.abspath(__file__))
    fname = "day{0}_input.txt".format(day)
    infile = os.path.join(indir, fname)
    with open(infile, 'r') as f:
        if call_func:
            return call_func(f)
        return [x.strip() for x in f.readlines()]