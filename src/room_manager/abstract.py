from utils import get_first_spawn


class AbstractRoomManager:
    BUILD_SCHEDULE = 100  # try to build once every n ticks
    SPAWN_SCHEDULE = 10
    DEBUG_VIS = dict({
        STRUCTURE_ROAD: {'stroke': '#00ff00'},
        STRUCTURE_EXTENSION: {'stroke': 'yellow'},
        STRUCTURE_CONTAINER: {'stroke': '#0000ff'},
        STRUCTURE_TOWER: {'stroke': '#ff0000'},
    })
    def __init__(self, room, name, creep_registry, enable_building):
        self.room = room
        self.name = name
        self.creep_registry = creep_registry
        self.enable_building = enable_building

    def run(self):
        if self.creep_registry.count_of_type(self.room, 'harvester') == 0 and self.creep_registry.count_of_type(self.room, 'builder') == 0:
            # everyone died :|
            if self.room.energyAvailable < 550:
                # we either are in RCL1 anyway or we are RCL2 but nobody will fill spawn/extensions, lets just get someone to do that
                #return RoomManagerRCL1().spawn_creeps()
                if self.room.energyAvailable >= 250:  # wait until source is full (there are no extensions)
                    spawn = get_first_spawn(self.room)
                    spawn.createCreep([WORK, CARRY, MOVE, MOVE], "", {'cls': 'harvester'})

        if self.name != 'sim':
            room_id = int(self.room.controller.id)
        else:
            room_id = 0  # int(id) doesn't work in sim?

        if Game.time % self.SPAWN_SCHEDULE == (room_id+1) % self.SPAWN_SCHEDULE:
            self.spawn_creeps()
        if Game.time % self.BUILD_SCHEDULE == room_id % self.BUILD_SCHEDULE or not self.enable_building:
            print('running build planner for', self.name, self.enable_building)
            self.run_build()
        action_sets = []
        return action_sets

    def spawn_creeps(self):
        raise NotImplementedError

    def run_build(self):
        raise NotImplementedError

    def build(self, structure_type, x, y, draw=True):
        pos = self.room.getPositionAt(x, y)
        if self.enable_building:
            pos.createConstructionSite(structure_type)
        elif draw:
            self.room.visual.circle(pos, self.DEBUG_VIS.get(structure_type, {'stroke': 'red'}))
        return pos

    def build_road(self, x, y, draw=True):
        return self.build(STRUCTURE_ROAD, x, y, draw)

    def build_roads(self, points):
        if self.enable_building:
            for point in points:
                self.build_road(point.x, point.y, False)
        else:
            self.room.visual.poly(
                [(pos.x, pos.y) for pos in points],
                self.DEBUG_VIS.get(
                    STRUCTURE_ROAD,
                    {'stroke': 'red'},
                )
            )

    def build_extension(self, x, y):
        return self.build(STRUCTURE_EXTENSION, x, y)

    def build_container(self, x, y):
        return self.build(STRUCTURE_CONTAINER, x, y)
