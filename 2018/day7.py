import re
from string import ascii_uppercase
from collections import defaultdict

from commonlib import determine_day, read_input_data


DAY = determine_day(__file__)
SAMPLE_DATA = [
    'Step C must be finished before step A can begin.',
    'Step C must be finished before step F can begin.',
    'Step A must be finished before step B can begin.',
    'Step A must be finished before step D can begin.',
    'Step B must be finished before step E can begin.',
    'Step D must be finished before step E can begin.',
    'Step F must be finished before step E can begin.',
]


def parse_dependencies(in_data):
    steps = set()
    dependencies = defaultdict(list)
    regex = re.compile(r"Step\s(?P<catalyst>[A-Z]).+step\s(?P<step>[A-Z]).+")
    for line_no, line in enumerate(in_data):
        res = regex.match(line)
        if not res:
            print("Error parsing line #{0}: {1}".format(line_no, line))
            continue
        steps.add(res['catalyst'])
        dependencies[res['step']].append(res['catalyst'])
    for step in steps:
        if step not in dependencies:
            dependencies[step] = []
    return dict([(s, sorted(c)) for (s, c) in dependencies.items()])


def sort_by_catalysts(dependencies):
    by_catalysts = []
    # Sort dependencies by lenth of value then their key
    for s, a in sorted(dependencies.items(), key=lambda kv: (len(kv[1]), kv[0])): 
        by_catalysts.append((s, a))
    return by_catalysts


def queue_ready_steps(by_catalysts, completed):
    ready = []
    for step, catalysts in by_catalysts:
        if step in completed:
            continue
        if (len(catalysts) == 0 and step not in completed) or \
            all((s in completed) for s in catalysts):
            ready.append(step)
    return ready


def determine_step_order(dependencies):
    completed = []
    by_catalysts = sort_by_catalysts(dependencies)

    queue = set()
    while len(completed) != len(dependencies):
        queue.update(queue_ready_steps(by_catalysts, completed))
        next_step = sorted(queue).pop(0)
        completed.append(next_step)
        queue.remove(next_step)
    return completed


def simulate_worker_queue(dependencies, workers=5, add_sec=60):
    by_catalysts = sort_by_catalysts(dependencies)
    task_queue = set()
    completed = []
    assigned = []
    # Worker 0 == "Me"
    worker_queue = dict((x, None) for x in range(0, workers))
    # Map task to its expected taks time
    task_time = dict((ta, ti) for (ti, ta) in enumerate(ascii_uppercase, start=add_sec+1))

    def _ready_workers():
        return [x for x in worker_queue if worker_queue[x] is None]

    def _assign_task(task, wid):
        worker_queue[wid] = [task, task_time[task]]
        return task

    def _tick_time_down():
        tasks_done = []
        for wid, task in worker_queue.items():
            if task is None:
                continue
            task[1] -= 1
            if task[1] == 0:
                tasks_done.append(task[0])
                worker_queue[wid] = None
        return tasks_done
    
    time_spent = 0
    while len(completed) != len(dependencies):
        # Check for ready tasks, aka their order based on completed tasks
        task_queue.update(queue_ready_steps(by_catalysts, completed))
        # But avoid re-assigned currently assigned tasks
        task_queue = task_queue.difference(set(assigned))
        # If no available workers or takss, then there's no point
        # in doing the extra work to figure tasks + assigning
        if _ready_workers() and task_queue:
            for wid in _ready_workers():
                if task_queue:
                    # Assign the next task and remove it from queue
                    task = _assign_task(sorted(task_queue)[0], wid)
                    assigned.append(task)
                    task_queue.remove(task)
        # Tick down the time
        completed.extend(_tick_time_down())
        time_spent += 1
    return time_spent, completed


def exec_day(sample=False):
    if sample:
        in_data = SAMPLE_DATA
        workers = 2
        add_sec = 0
    else:
        in_data = read_input_data(DAY)
        workers = 5
        add_sec = 60
    
    dependencies = parse_dependencies(in_data)

    p1 = determine_step_order(dependencies)
    print("Part 1:", ''.join(p1))

    p2 = simulate_worker_queue(dependencies, workers=workers, add_sec=add_sec)
    print("Part 2:", p2[0], ''.join(p2[1]))

