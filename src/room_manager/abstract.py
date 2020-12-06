__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')

from utils import get_first_spawn

g_links = dict()


class AbstractRoomManager:
    BUILD_SCHEDULE = 100  # try to build once every n ticks
    SPAWN_SCHEDULE = 10
    LINKS_SCHEDULE = 1
    DEBUG_VIS = dict({
        STRUCTURE_ROAD: {'stroke': '#00ff00'},
        STRUCTURE_EXTENSION: {'stroke': 'yellow'},
        STRUCTURE_CONTAINER: {'stroke': '#0000ff'},
        STRUCTURE_TOWER: {'stroke': '#ff0000'},
    })
    def __init__(self, room, creep_registry, enable_building):
        self.room = room
        self.creep_registry = creep_registry
        self.enable_building = enable_building
        #self.enable_building = False  # TODO: build the spawn itself, then abort?

    def run(self):
        harvesters = self.creep_registry.count_of_type(self.room, 'harvester')
        builders = self.creep_registry.count_of_type(self.room, 'builder')
        haulers = self.creep_registry.count_of_type(self.room, 'hauler')
        miners = self.creep_registry.count_of_type(self.room, 'miner')
        if harvesters == 0 and builders == 0 and (haulers == 0 or miners == 0):
            spawn = get_first_spawn(self.room)
            # everyone died :|
            if self.room.energyAvailable < 550:
                # we either are in RCL1 anyway or we are RCL2 but nobody will fill spawn/extensions, lets just get someone to do that
                #return RoomManagerRCL1().spawn_creeps()
                if self.room.energyAvailable >= 250:  # wait until source is full (there are no extensions)
                    spawn = get_first_spawn(self.room)
                    spawn.createCreep([WORK, CARRY, MOVE, MOVE], "", {'cls': 'harvester'})

        if self.room.name != 'sim':
            room_id = int(self.room.controller.id)
        else:
            room_id = 0  # int(id) doesn't work in sim?

        if Game.time % self.SPAWN_SCHEDULE == (room_id+1) % self.SPAWN_SCHEDULE:
            self.spawn_creeps()

        our_links = g_links.get(self.room.name)
        if Game.time % self.BUILD_SCHEDULE == room_id % self.BUILD_SCHEDULE or not self.enable_building or our_links == undefined:
            print('running build planner for', self.room.name, self.enable_building)  # XXX
            self.run_build()
            return []  # we have to return because the link cache doesn't work yet

        if self.room.controller.level >= 5 and Game.time % self.LINKS_SCHEDULE == (room_id+1) % self.LINKS_SCHEDULE:
            if len(g_links) and our_links != undefined:  # build scheduler updates it
                self.run_links(our_links)
            else:
                print('WARNING: not running links in', self.room.name, 'because they were not cached yet')
                # TODO: haxxx pff
                #self.run_build()
                # sadly, it doesn't work
                #our_links = g_links.get(self.room.name)
                #self.run_links(our_links)
        action_sets = []
        return action_sets

    def run_links(self, our_links):
        controller_link = our_links.get_controller()
        if not controller_link:
            return
        #print('============================ running links in', self.room.name, our_links, our_links.get_controller())
        if controller_link.store[RESOURCE_ENERGY] <= 50:
            print('////////////////////////////', self.room.name, 'controller needs link filled', our_links.get_sources())
            for source_link in our_links.get_sources():
                if source_link.store[RESOURCE_ENERGY] == LINK_CAPACITY:
                    source_link.transferEnergy(controller_link, controller_link.store.getFreeCapacity(RESOURCE_ENERGY))
                    print('++++++++++++++++++++++++++++ transfer energy from', source_link, 'to', controller_link)
                    break
                else:
                    print('----------------------------', source_link, 'does not have enough to send to controller', source_link.store[RESOURCE_ENERGY])

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
