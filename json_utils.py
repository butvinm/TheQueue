import json


def add_queue(queue_name: str) -> bool:
    """True if new created, False if already exists"""

    with open('./queues.json', 'r') as f:
        data = json.load(f)

    if queue_name in data:
        return False

    data[queue_name] = []
    with open('./queues.json', 'w') as f:
        json.dump(data, f)

    return True


def remove_queue(queue_name: str) -> bool:
    """True if removed, False if does not exist"""

    with open('./queues.json', 'r') as f:
        data = json.load(f)

    if queue_name not in data:
        return False
    
    data.pop(queue_name)
    with open('./queues.json', 'w') as f:
        json.dump(data, f)

    return True


def add_to_queue(queue_name: str, full_name: str) -> int:
    """Positive position in queue if new added, -2 if full_name already exists, -1 if queue does not exist"""

    with open('./queues.json', 'r') as f:
        data = json.load(f)

    if queue_name not in data:
        return -1
    
    if full_name in data[queue_name]:
        return -2
    
    data[queue_name].append(full_name)
    with open('./queues.json', 'w') as f:
        json.dump(data, f)

    return len(data[queue_name])


def remove_from_queue(queue_name: str, full_name: str) -> int:
    """Current len of queue if removed, -2 if full_name does not exists, -1 if queue does not exist"""

    with open('./queues.json', 'r') as f:
        data = json.load(f)

    if queue_name not in data:
        return -1
    
    if full_name not in data[queue_name]:
        return -2
    
    data[queue_name].remove(full_name)
    with open('./queues.json', 'w') as f:
        json.dump(data, f)

    return len(data[queue_name])


def get_queue_members(queue_name: str) -> list[str]:
    """Return list of queue members or None if queue does not exist"""

    with open('./queues.json', 'r') as f:
        data = json.load(f)
    
    return data.get(queue_name, None)


def get_queues() -> dict[str, list[str]]:
    with open('./queues.json', 'r') as f:
        data = json.load(f)
    
    return data


def get_me_at(queue_name: str, full_name: str) -> int:
    """-1 if queue not exist, -2 if not consist, else position"""

    with open('./queues.json', 'r') as f:
        data = json.load(f)
    
    if queue_name not in data:
        return -1
    
    if full_name not in data[queue_name]:
        return -2

    return data[queue_name].index(full_name) + 1


def get_me_all(full_name: str) -> dict[str, int]:
    with open('./queues.json', 'r') as f:
        data = json.load(f)
    
    result = {}
    for q_name in data:
        pos = get_me_at(q_name, full_name)
        print(q_name, pos)
        if pos >= 0:
            result[q_name] = pos

    return result
