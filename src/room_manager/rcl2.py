from utils import get_first_spawn
from utils import get_thing_at_coordinates
from utils import search_room

from room_manager.abstract import AbstractRoomManager
from room_manager.rcl1 import RoomManagerRCL1


class RoomManagerRCL2(AbstractRoomManager):
    def spawn_creeps(self):
        room = self.room
        spawn = get_first_spawn(room)
        if not spawn.spawning:
            if room.energyCapacityAvailable < 550:  # extensions were not built yet
                return self.spawn_creeps_in_transition_period()
            elif self.creep_registry.count_of_type(room, 'builder') < 1:  # TODO: how many builders depends on site count
                # builders first to make containers for mining
                if room.energyAvailable >= 550:
                    spawn.createCreep([WORK, WORK, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE], "", {'cls': 'builder'})
            elif self.creep_registry.count_of_type(room, 'miner') < 2: #TODO len(room.sources):  # 2
                if room.energyAvailable >= 550:
                    spawn.createCreep([WORK, WORK, WORK, WORK, WORK, MOVE], "", {'cls': 'miner'})
            #elif self.creep_registry.count_of_type(room, 'hauler') < 2: #TODO len(room.sources):  # TODO: ? 2
            #    if room.energyAvailable >= 550:
            #        spawn.createCreep([WORK, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE, MOVE], "", {'cls': 'hauler'})
            elif self.creep_registry.count_of_type(room, 'hauler') < 1:
                if room.energyAvailable >= 550:
                    # TODO: scale it to the room size
                    parts = [CARRY, CARRY, CARRY, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE]
                    spawn.createCreep(parts, "", {'cls': 'hauler'})
                    return
            elif self.creep_registry.count_of_type(room, 'upgrader') < 12:  # TODO: ? 3
                if room.energyAvailable >= 550:
                    spawn.createCreep([WORK, WORK, WORK, WORK, CARRY, MOVE, MOVE], "", {'cls': 'upgrader'})
            # total of 7, so 0.2*7 = 1.4 CPU/tick - decisions

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
    def build(self):
        # TODO: don't do it every tick
        room = self.room
        # shaped farms first
        if room.energyCapacityAvailable < 550:  # all extensions were not built yet
            #eree
            # ere
            #   r
            #   S
            spawn_pos = get_first_spawn(room).pos
            # TODO: don't do that if site is already here
            room.getPositionAt(spawn_pos.x,   spawn_pos.y-2).createConstructionSite(STRUCTURE_EXTENSION)
            room.getPositionAt(spawn_pos.x,   spawn_pos.y-3).createConstructionSite(STRUCTURE_EXTENSION)
            room.getPositionAt(spawn_pos.x-1, spawn_pos.y-3).createConstructionSite(STRUCTURE_EXTENSION)
            room.getPositionAt(spawn_pos.x-2, spawn_pos.y-2).createConstructionSite(STRUCTURE_EXTENSION)
            room.getPositionAt(spawn_pos.x-3, spawn_pos.y-3).createConstructionSite(STRUCTURE_EXTENSION)

            room.getPositionAt(spawn_pos.x,   spawn_pos.y-1).createConstructionSite(STRUCTURE_ROAD)
            room.getPositionAt(spawn_pos.x-1, spawn_pos.y-2).createConstructionSite(STRUCTURE_ROAD)
            room.getPositionAt(spawn_pos.x-2, spawn_pos.y-3).createConstructionSite(STRUCTURE_ROAD)
            return
        # TODO: build roads automatically using self.creep_registry that has room stats and routes

        sources = search_room(room, FIND_SOURCES)
        containers = search_room(room, FIND_STRUCTURES, lambda x: x.structureType == STRUCTURE_CONTAINER)
        if len(containers) == len(sources) + 1:
            return
        container_sites = search_room(room, FIND_CONSTRUCTION_SITES, lambda x: x.structureType == STRUCTURE_CONTAINER)
        if len(containers) + len(container_sites) == len(sources) + 1:
            return

        for source in sources:
            path = room.findPath(source.pos, room.controller.pos, {'ignoreCreeps': True})
            thing = get_thing_at_coordinates(containers, path[0].x, path[0].y)
            if thing:
                continue
            thing = get_thing_at_coordinates(container_sites, path[0].x, path[0].y)
            if thing:
                continue
            print('path[0]', path[0])
            room.getPositionAt(path[0].x,   path[0].y).createConstructionSite(STRUCTURE_CONTAINER)

        # build a container next to controller
        path = room.findPath(room.controller.pos, get_first_spawn(room).pos, {'ignoreCreeps': True})
        thing = get_thing_at_coordinates(containers, path[1].x, path[1].y)
        if thing:
            return
        thing = get_thing_at_coordinates(container_sites, path[1].x, path[1].y)
        if thing:
            return
        room.getPositionAt(path[1].x, path[1].y).createConstructionSite(STRUCTURE_CONTAINER)

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
