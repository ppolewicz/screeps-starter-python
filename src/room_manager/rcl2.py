__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')

from utils import get_first_spawn
from utils import get_controller_spawn
from utils import search_room
from utils import P
from utils import around_range

from room_manager.abstract import AbstractRoomManager
from room_manager.links import Links
from room_manager.abstract import g_links
from room_manager.rcl1 import RoomManagerRCL1


room_sizes = {}  # TODO: global memory


class RoomManagerRCL2(AbstractRoomManager):
    def spawn_creeps(self):
        room = self.room
        spawn = get_first_spawn(room)
        if spawn is None:
            return  # no spawn yet
        if not spawn.spawning:
            if room.energyCapacityAvailable < 550:  # extensions were not built yet
                return self.spawn_creeps_in_transition_period()

            to_construct = [s.progressTotal - s.progress for s in room.find(FIND_CONSTRUCTION_SITES)]
            to_construct_sum = sum(to_construct)
            builders = self.creep_registry.count_of_type(room, 'builder')
            miners = self.creep_registry.count_of_type(room, 'miner')
            haulers = self.creep_registry.count_of_type(room, 'hauler')
            dropped_sum = sum([r.amount for r in room.find(FIND_DROPPED_RESOURCES)])
            size = room_sizes[room]
            if size == undefined:  # TODO: fill it aggresively, don't wait
                size = 25
            #print('room size', room, size)
            desired_haulers = int(size / 10)  # TODO: can use less larger ones
            if room.controller.level >= 5:
                desired_haulers = 3  # TODO: when miners will man the links, we can reduce that to 1
            if to_construct_sum > 12000 and builders < 5 and miners >= 1 or \
               to_construct_sum > 9000 and builders < 4 and miners >= 1 or \
               to_construct_sum > 6000 and builders < 3 and miners >= 1 or \
               to_construct_sum > 3000 and builders < 2 or \
               to_construct_sum > 0 and builders < 1:
                # builders first to make containers for mining
                to_construct_max = max(to_construct)
                to_construct_avg = sum(to_construct) / len(to_construct)
                if room.energyAvailable >= 550:
                    if to_construct_max >= 5001:
                        parts = [WORK, WORK, WORK, CARRY, MOVE, MOVE, MOVE, MOVE]
                    elif to_construct_avg >= 5001:
                        parts = [WORK, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE, MOVE]
                    else:
                        parts = [WORK, WORK, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE]
                    spawn.createCreep(parts, "", {'cls': 'builder'})
            elif miners < 2:  #TODO number of sources
                if room.controller.level <= 4 or True:  # TODO
                    if room.energyAvailable >= 2200:
                        spawn.createCreep([WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, MOVE, MOVE, MOVE, MOVE], "", {'cls': 'miner'})
                    elif room.energyAvailable >= 1650:
                        spawn.createCreep([WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, MOVE, MOVE, MOVE], "", {'cls': 'miner'})
                    elif room.energyAvailable >= 1100:
                        spawn.createCreep([WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, MOVE, MOVE], "", {'cls': 'miner'})
                    elif room.energyAvailable >= 550:
                        spawn.createCreep([WORK, WORK, WORK, WORK, WORK, MOVE], "", {'cls': 'miner'})
                else:  # link miners
                    if room.energyAvailable >= 3900:  # this one is optimized for CPU, really
                        spawn.createCreep([
                            WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK,
                            WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK,
                            WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK,
                            CARRY, CARRY, CARRY, CARRY, CARRY, CARRY,
                            CARRY, CARRY, CARRY, CARRY, CARRY, CARRY,
                            MOVE, MOVE, MOVE, MOVE, MOVE, MOVE,  # TODO: they should spawn on the position and never move
                        ], "", {'cls': 'miner'})
                    elif room.energyAvailable >= 3600:
                        spawn.createCreep([  # TODO: those should be calculated by math from energyAvailable, not templated
                            WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK,
                            WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK,
                            WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK,
                            CARRY, CARRY, CARRY, CARRY, CARRY, CARRY,
                            MOVE, MOVE, MOVE, MOVE, MOVE, MOVE,
                        ], "", {'cls': 'miner'})
                    elif room.energyAvailable >= 2400:
                        spawn.createCreep([
                            WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK,
                            WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK,
                            CARRY, CARRY, CARRY, CARRY,
                            MOVE, MOVE, MOVE, MOVE,
                        ], "", {'cls': 'miner'})
                    elif room.energyAvailable >= 1800:
                        spawn.createCreep([WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE], "", {'cls': 'miner'})
                    elif room.energyAvailable >= 1200:
                        spawn.createCreep([WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, CARRY, CARRY, MOVE, MOVE], "", {'cls': 'miner'})
                    elif room.energyAvailable >= 600:
                        spawn.createCreep([WORK, WORK, WORK, WORK, WORK, CARRY, MOVE], "", {'cls': 'miner'})
                    elif room.energyAvailable >= 550:
                        spawn.createCreep([WORK, WORK, WORK, WORK, WORK, MOVE], "", {'cls': 'miner'})
            #elif self.creep_registry.count_of_type(room, 'hauler') < 2: #TODO len(room.sources):  # TODO: ? 2
            #    if room.energyAvailable >= 550:
            #        spawn.createCreep([WORK, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE, MOVE], "", {'cls': 'hauler'})
            #elif dropped_sum > 5000 and haulers < 5 or \
            #     dropped_sum > 1000 and haulers < 4 or \
            #     dropped_sum > 50 and haulers < 3 or \
            #     haulers < 2:
            elif haulers < desired_haulers:
                if room.energyAvailable >= 550:
                    # TODO: scale it to the room size
                    #parts = [CARRY, CARRY, CARRY, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE]
                    parts = [WORK, CARRY, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE]
                    spawn.createCreep(parts, "", {'cls': 'hauler'})
                    return


            # upgraders

            if to_construct > 300:
                return

            #  eee
            # 12fe
            # 1M2e
            # E11
            #
            # E: source
            # M: miner
            # f: filler
            # e: extension
            # 1: accessible only to Miner: tower, terminal
            # 2: accessible to both Miner and Filler: spawn, storage
            # please note that it would be best for terminal and storage to be accessible. Also Spawn(2) must be accessible.
            spawn = get_controller_spawn(room)
            if room.energyCapacityAvailable >= 100*15 +50*3 +50*5:
                spawn_it = False
                if self.creep_registry.count_of_type(room, 'upgrader') < 1:
                    spawn_it = True
                else:
                    prespawn = 23 * CREEP_SPAWN_TIME
                    upgrader = self.creep_registry.list_of_type('upgrader')[0]
                    if upgrader.ticksToLive <= prespawn:
                        spawn_it = True
                if spawn_it:
                    spawn.createCreep(
                        [
                            WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK,
                            CARRY, CARRY, CARRY,  # get even more?
                            MOVE, MOVE, MOVE, MOVE, MOVE,  # TODO: could save 250 energy / 1500 tics here if we spawned the guy and immediately moved him where he belongs
                        ],
                        "",
                        {
                            'memory': {'cls': 'upgrader'},
                            # TODO: take energy from spawns first
                            # TODO: 'directions': [TOP_RIGHT],
                        }
                    )
                if room.controller.level == 8:
                    return
            elif room.energyCapacityAvailable >= 950:
                if self.creep_registry.count_of_type(room, 'upgrader') < 2:
                    spawn.createCreep([WORK, WORK, WORK, WORK, WORK, WORK, WORK, WORK, CARRY, MOVE, MOVE], "", {'cls': 'upgrader'})
            elif room.energyCapacityAvailable >= 650:
                if self.creep_registry.count_of_type(room, 'upgrader') < 3:
                    spawn.createCreep([WORK, WORK, WORK, WORK, WORK, CARRY, MOVE, MOVE], "", {'cls': 'upgrader'})
            elif room.energyCapacityAvailable >= 550:
                if self.creep_registry.count_of_type(room, 'upgrader') < 4:
                    spawn.createCreep([WORK, WORK, WORK, WORK, CARRY, MOVE, MOVE], "", {'cls': 'upgrader'})

    def spawn_creeps_in_transition_period(self):
        room = self.room
        spawn = get_first_spawn(room)
        if room.energyCapacityAvailable >= 500:
            if self.creep_registry.count_of_type(room, 'harvester') < RoomManagerRCL1.MAX_HARVESTERS:  # keep spawning them, why not
                if room.energyAvailable >= 500:
                    spawn.createCreep([WORK, WORK, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE], "", {'cls': 'harvester'})
        elif room.energyCapacityAvailable >= 450:
            if self.creep_registry.count_of_type(room, 'harvester') < RoomManagerRCL1.MAX_HARVESTERS:  # keep spawning them, why not
                if room.energyAvailable >= 450:
                    spawn.createCreep([WORK, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE], "", {'cls': 'harvester'})
        elif room.energyCapacityAvailable >= 350:
            if self.creep_registry.count_of_type(room, 'harvester') < RoomManagerRCL1.MAX_HARVESTERS:  # keep spawning them, why not
                if room.energyAvailable >= 350:
                    spawn.createCreep([WORK, CARRY, CARRY, MOVE, MOVE, MOVE], "", {'cls': 'harvester'})
        else:
            return RoomManagerRCL1(room, self.creep_registry).spawn_creeps()  # keep RCL1 layout until they build up the extensions

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
    def run_build(self):
        # TODO: don't do it every tick
        room = self.room
        spawn = get_first_spawn(room)
        if spawn is None:
            #return  # no spawn yet and no construction site.
            return
            #spawn_pos = room.getPositionAt(8, 21)
        else:
            spawn_pos = spawn.pos

        # shaped farms first
        if room.energyCapacityAvailable < 550:  # all extensions were not built yet
            #eree
            # ere
            #   r
            #   S

            self.build_extension(spawn_pos.x,   spawn_pos.y-2)
            self.build_extension(spawn_pos.x,   spawn_pos.y-3)
            self.build_extension(spawn_pos.x-1, spawn_pos.y-3)
            self.build_extension(spawn_pos.x-2, spawn_pos.y-2)
            self.build_extension(spawn_pos.x-3, spawn_pos.y-3)
            if self.enable_building:
                return

        self.build_roads(
            [
                P(spawn_pos.x,   spawn_pos.y-1),
                P(spawn_pos.x-1, spawn_pos.y-2),
                P(spawn_pos.x-2, spawn_pos.y-3),
            ]
        )

        sources = search_room(room, FIND_SOURCES)

        map_size = 0
        miner_containers = []
        for source in sources:
            path = room.findPath(source.pos, room.controller.pos, {'ignoreCreeps': True})
            map_size += len(path)
            miner_containers.append(
                self.build_container(path[0].x, path[0].y)
            )
        room_sizes[room] = map_size

        def costCallback(roomName, costMatrix):
            terrain = Game.rooms[roomName].getTerrain()
            around_coords = around_range(room, room.controller.pos.x, room.controller.pos.y, 1)
            around_coords.extend(
                around_range(room, room.controller.pos.x, room.controller.pos.y, 2)
            )
            walls = []
            for x, y in around_coords:
                if terrain.get(x, y) == 1:
                    walls.append((x, y))
            for wx, wy in walls:
                for x, y in around_range(room, wx, wy, 1):
                    costMatrix.set(x, y, 20)

            #    value = 70
            #        value = 255
            #    costMatrix.set(x, y, value)
            #for x, y in around_range(room, room.controller.pos.x, room.controller.pos.y, 2):
            #    value = 40
            #    if terrain.get(x, y) == 1:
            #        value = 255
            #    costMatrix.set(x, y, value)
            #costMatrix.set(18, 8, 50)

        #PathFinder.use(True)
        # build a container next to controller
        path = room.findPath(
            room.controller.pos,
            spawn_pos,
            {
                'ignoreCreeps': True,
                'costCallback': costCallback,
                'maxRooms': 1,
            },
        )
        controller_container = room.getPositionAt(path[1].x, path[1].y)

        self.build_container(path[1].x, path[1].y)

        roads = []
        #if 1:
        #    roads.append(path)
        #    #return

        ignoreRoads = True
        for miner_container in miner_containers:
            path = room.findPath(miner_container, controller_container, {'ignoreCreeps': True, 'ignoreRoads': ignoreRoads})
            roads.append(path[0:len(path)-1])
            path = room.findPath(miner_container, spawn_pos, {'ignoreCreeps': True})
            roads.append(path[0:len(path)-1])

        links = Links()
        link_filter = lambda s: (
            s.structureType == STRUCTURE_LINK
        )
        for what, obj in [
                ('controller', room.controller),
                ('storage', room.storage),
                ('terminal', room.terminal),
                # TODO: mineral link
            ]:
            if obj == undefined:
                #print(what, 'does not exist in', room.name)
                continue
            structures = obj.pos.findInRange(FIND_STRUCTURES, 3, filter=link_filter)  # TODO: if faith source is close to energy source, this will mess up
            if len(structures) >= 1:
                setattr(links, what + '_id', structures[0].id)
            #else:
            #    print('no link for', what, 'in', room)

        for miner_container in miner_containers:
            miner_links = miner_container.findInRange(FIND_STRUCTURES, 1, filter=link_filter)
            if len(miner_links):
                links.source_ids.append(miner_links[0].id)

        #print('setting links', links, 'in', room)
        g_links[room.name] = links

        #print('road', roads[0][1])
        #room.visual.poly(roads[0][1], {'color': 'ff0000'})
        #print(roads[0][1][0], roads[0][1][len(roads[0][1]-1)])
        #room.getPositionAt(roads[0][1][0].x, roads[0][1][0].y)
        roads.sort(key=lambda road: -1*len(road))
        #for road in roads:
        #    room.visual.poly([(point.x, point.y) for point in road], {'stroke': '#00ff00'})

        #for s in room.find(FIND_STRUCTURES):
        #    if s.structureType == STRUCTURE_ROAD:
        #        s.destroy()

        built_something = False
        for road in roads:
            for point in road:
                has_road = False
                for s in room.lookForAt(LOOK_STRUCTURES, point.x, point.y):
                    if s.structureType == STRUCTURE_ROAD and s.hits >= 1:
                        has_road = True
                        break
                if not has_road or not self.enable_building:
                    built_something = True
            if built_something:
                self.build_roads(road)
                if self.enable_building:
                    break  # build roads incrementally




#            break
#            candidate_spots = []
#            source_is_covered = False
#            print('room', room)
#            terrain = room.getTerrain()
#            print('terrain', terrain)
#            print('terrain.get', terrain.get)
#            return
#            terrain2 = Game.map.getRoomTerrain(room.name)
#            print('terrain2', terrain2)
#
#            print('terrain.get(1, 1)', terrain.get(15, 15))
#            #print('terrain2.get', terrain2.get)
#            #.get(1, 1)
#            for x_diff, y_diff in self.AROUND_OFFSETS:
#                print('offsets', x_diff, y_diff)
#                x = source.pos.x + x_diff
#                y = source.pos.y + y_diff
#                print('terrain', dict(terrain))
#                content = terrain.get(x, y)
#                print('content for x,y', x, y, content)
#                if content == 1:  # wall
#                    continue
#                thing = get_thing_at_coordinates(containers, x, y)
#                if thing:
#                    source_is_covered = True
#                    break
#                thing = get_thing_at_coordinates(container_sites, x, y)
#                if thing:
#                    source_is_covered = True
#                    break
#                candidate_spots.append((x, y))
#            if source_is_covered:
#                continue
#            print('uncovered source:', source, len(candidate_spots))
#            #if len(candidate_spots) == 1:
#            #    pass
#            # for each free space around source
#            # sort the list by distance to controller
#            # is container on that space already?
#            #     continue
#            # build a container
#
