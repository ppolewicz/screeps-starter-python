__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')

from utils import get_first_spawn
from utils.errors import ERRORS

g_links = dict()


class AbstractRoomManager:
    BUILD_SCHEDULE = 100  # try to build once every n ticks
    SPAWN_SCHEDULE = 10
    LINKS_SCHEDULE = 1
    LINK_MIN_TRANSFER_AMOUNT = LINK_CAPACITY / 4
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
        if our_links == undefined:
            Game.notify(
                'Global reset detected at ' + self.room.name + ', current bucket: ' + str(Game.cpu.bucket),
                60,  # group these notifications for X min
            )
        if Game.time % self.BUILD_SCHEDULE == room_id % self.BUILD_SCHEDULE or not self.enable_building or our_links == undefined:
            print('running build planner for', self.room.name, self.enable_building)
            self.run_build()
            #return []  # we have to return here because the link cache doesn't work yet for some reason

        if self.room.controller.level >= 5 and Game.time % self.LINKS_SCHEDULE == (room_id+1) % self.LINKS_SCHEDULE:
            if len(g_links) >= 1 and our_links != undefined:  # build scheduler updates it
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

    def debug_log(self, *args):
        DEBUG_ROOMS = []
        #DEBUG_ROOMS = ['W24N2']
        if DEBUG_ROOMS.includes(self.room.name):
            print(*args)

    def run_links(self, our_links):
        controller_link = our_links.get_controller()
        if not controller_link:
            return
        target_links = []
        if self.room.energyCapacityAvailable > 0:
            # sources send to others, then controller
            source_links = our_links.get_sources()
            target_links.extend(our_links.get_others())
            target_links.append(controller_link)
        else:
            # sources and others feed controller
            target_links.append(controller_link)
            source_links = our_links.get_sources()
            source_links.extend(our_links.get_others())
        self.debug_log('============================ running links in', self.room.name, our_links)
        used_set = set()
        done = self.execute_transfer(source_links, target_links, used_set)

    def execute_transfer(self, source_links, target_links, used_set):
        for target_link in target_links:
            self.debug_log('target_link', target_link.id)
            if target_link.store.getFreeCapacity(RESOURCE_ENERGY) >= self.LINK_MIN_TRANSFER_AMOUNT:
                self.debug_log('////////////////////////////', target_link.id, 'link needs link filled')
                for source_link in source_links:
                    if source_link.cooldown != 0:
                        self.debug_log('source link', source_link.id, 'is on cooldown for', source_link.cooldown)
                        continue
                    if used_set.includes(source_link.id):
                        self.debug_log('source link', source_link.id, 'already used')
                        continue
                    if used_set.includes(target_link.id):
                        self.debug_log('WARNING: target link', target_link.id, 'already used!?')
                        continue
                    if source_link.store[RESOURCE_ENERGY] < self.LINK_MIN_TRANSFER_AMOUNT:
                        self.debug_log('source_link', source_link.id, 'does not have enough to send, it has:', source_link.store[RESOURCE_ENERGY])
                        continue
                    amount = min(
                        target_link.store.getFreeCapacity(RESOURCE_ENERGY),
                        source_link.store[RESOURCE_ENERGY],
                    )
                    error_code = source_link.transferEnergy(
                        target_link,
                        amount,
                    )
                    used_set.add(source_link.id)
                    used_set.add(target_link.id)
                    self.debug_log('++++++++++++++++++++++++++++ transfer energy from', source_link, 'to', target_link, ', error:', ERRORS[error_code])
                    return True
        return False

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
