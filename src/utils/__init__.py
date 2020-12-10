def part_count(creep, of_type):
    count = 0
    for part in creep.body:
        if part['type'] == of_type:
            count += 1
    return count

def get_first_spawn(room):
    for s in room.find(FIND_MY_STRUCTURES):
        if s.structureType == STRUCTURE_SPAWN:
            return s
    for s in room.find(FIND_CONSTRUCTION_SITES):
        if s.structureType == STRUCTURE_SPAWN:
            return s
    #print('WARNING: get_first_spawn returning None for', room)

def get_controller_spawn(room):
    # TODO: cache it and drop cache after a spawn is completed
    source_filter = lambda s: (
        s.structureType == STRUCTURE_SPAWN
    )
    return room.controller.pos.findClosestByRange(FIND_MY_STRUCTURES, filter=source_filter)

def search_room(room, kind, filter_function=lambda x: True):
    result_list = []
    for item in room.find(kind):
        if filter_function(item):
            result_list.append(item)
    return result_list


def get_thing_at_coordinates(things, x, y):
    for thing in things:
        if x == thing.pos.x and y == thing.pos.y:
            return thing

class P:
    def __init__(self, x, y):
        self.x = x
        self.y = y


ERRORS = {
    0: 'OK',
    -1: 'ERR_NOT_OWNER',
    -2: 'ERR_NO_PATH',
    -3: 'ERR_NAME_EXISTS',
    -4: 'ERR_BUSY',
    -5: 'ERR_NOT_FOUND',
    -6: 'ERR_NOT_ENOUGH_ENERGY/RESOURCES/EXTENSIONS',
    -7: 'ERR_INVALID_TARGET',
    -8: 'ERR_FULL',
    -9: 'ERR_NOT_IN_RANGE',
    -10: 'ERR_INVALID_ARGS',
    -11: 'ERR_TIRED',
    -12: 'ERR_NO_BODYPART',
    -14: 'ERR_RCL_NOT_ENOUGH',
    -15: 'ERR_GCL_NOT_ENOUGH',
}

AROUND_OFFSETS = (
    (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, 1),
        (0, -1),
        (1, -1),
        (1, 0),
        (1, 1),
    ),
    (
        (1, -2),
        (0, -2),
        (-1, -2),
        (-2, -2),
        (-2, -1),
        (-2, 0),
        (-2, 1),
        (-2, 2),
        (-1, 2),
        (0, 2),
        (1, 2),
        (2, -2),
        (2, -1),
        (2, 0),
        (2, 1),
        (2, 2),
    ),
)


def around_range(room, x, y, distance, vis=None):
    result = []
    for x_diff, y_diff in AROUND_OFFSETS[distance-1]:
        result.append((x + x_diff, y + y_diff))
        if vis is not None:
            room.visual.circle(x+x_diff, y+y_diff, {'stroke': vis})
    return result
