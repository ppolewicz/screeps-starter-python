from utils import get_first_spawn
from utils import search_room
from utils import P

from room_manager.abstract import AbstractRoomManager
from room_manager.rcl1 import RoomManagerRCL1


class RoomManagerRCL2(AbstractRoomManager):
    def spawn_creeps(self):
        room = self.room
        spawn = get_first_spawn(room)
        if not spawn.spawning:
            if room.energyCapacityAvailable < 550:  # extensions were not built yet
                return self.spawn_creeps_in_transition_period()

            to_construct = sum([s.progressTotal - s.progress for s in room.find(FIND_CONSTRUCTION_SITES)])
            builders = self.creep_registry.count_of_type(room, 'builder')
            miners = self.creep_registry.count_of_type(room, 'miner')
            if to_construct > 12000 and builders < 5 and miners >= 1 or \
               to_construct > 9000 and builders < 4 and miners >= 1 or \
               to_construct > 6000 and builders < 3 and miners >= 1 or \
               to_construct > 3000 and builders < 2 or \
               builders < 1:
                # builders first to make containers for mining
                if room.energyAvailable >= 550:
                    if to_construct > 6000:
                        parts = [WORK, WORK, WORK, CARRY, MOVE, MOVE, MOVE, MOVE]
                    else:
                        parts = [WORK, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE, MOVE]
                    spawn.createCreep(parts, "", {'cls': 'builder'})
            elif miners < 2:  #TODO len(room.sources):  # 2
                if room.energyAvailable >= 550:
                    spawn.createCreep([WORK, WORK, WORK, WORK, WORK, MOVE], "", {'cls': 'miner'})
            #elif self.creep_registry.count_of_type(room, 'hauler') < 2: #TODO len(room.sources):  # TODO: ? 2
            #    if room.energyAvailable >= 550:
            #        spawn.createCreep([WORK, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE, MOVE], "", {'cls': 'hauler'})
            elif self.creep_registry.count_of_type(room, 'hauler') < 2:
                if room.energyAvailable >= 550:
                    # TODO: scale it to the room size
                    parts = [CARRY, CARRY, CARRY, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE]
                    spawn.createCreep(parts, "", {'cls': 'hauler'})
                    return
            elif to_construct < 300 and self.creep_registry.count_of_type(room, 'upgrader') < 5:
                if room.energyAvailable >= 550:
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
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    )
    def run_build(self):
        # TODO: don't do it every tick
        room = self.room
        spawn_pos = get_first_spawn(room).pos
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

        miner_containers = []
        for source in sources:
            path = room.findPath(source.pos, room.controller.pos, {'ignoreCreeps': True})
            miner_containers.append(
                self.build_container(path[0].x, path[0].y)
            )

        # build a container next to controller
        path = room.findPath(room.controller.pos, spawn_pos, {'ignoreCreeps': True})
        controller_container = room.getPositionAt(path[1].x, path[1].y)

        self.build_container(path[1].x, path[1].y)

        roads = []
        for miner_container in miner_containers:
            path = room.findPath(miner_container, controller_container, {'ignoreCreeps': True})
            roads.append(path[0:len(path)-1])
            path = room.findPath(miner_container, spawn_pos, {'ignoreCreeps': True})
            roads.append(path[0:len(path)-1])

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
