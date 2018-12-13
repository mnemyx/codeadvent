import os
import argparse
from glob import glob
from importlib import util

from commonlib import determine_day


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
EXEC_FUNC = 'exec_day'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Execute Code Advent Days')
    parser.add_argument('-s', '--sample', action='store_true',
                        help='If flag exists, days will be executed'
                             'with sample data and not the actual input.')
    parser.add_argument('days', nargs='+',
                        help='Days to execute')
    args = parser.parse_args()

    days_re = os.path.join(THIS_DIR, 'day*.py')
    day_modules = glob(days_re)
    existing_days = [determine_day(x) for x in day_modules]
    mapped_days = dict(zip(existing_days, day_modules))

    for day in args.days:
        if day not in mapped_days:
            print(">>> SKIPPING UNAVAILABLE DAY: {0} <<<\n".format(day))
            continue

        spec = util.spec_from_file_location("day{0}".format(day), mapped_days[day])
        mod = util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        to_exec = getattr(mod, EXEC_FUNC)

        print("################ DAY {0} ################".format(day))
        to_exec(sample=args.sample)
        print("---------------------------------------\n")
