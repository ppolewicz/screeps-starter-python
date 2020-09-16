from utils import get_first_spawn
from room_manager.abstract import AbstractRoomManager
from room_manager.rcl1 import RoomManagerRCL1


class RoomManagerRCL2(AbstractRoomManager):
    def spawn_creeps(self):
        room = self.room
        spawn = get_first_spawn(room)
        if not spawn.spawning:
            if room.energyCapacityAvailable < 550:  # extensions were not built yet
                return RoomManagerRCL1(room, self.creep_registry).spawn_creeps()  # keep RCL1 layout until they build up the extensions
            if self.creep_registry.count_of_type(room, 'builder') < 4:  # TODO: all like this
                if room.energyAvailable >= 550:
                    spawn.createCreep([WORK, WORK, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE], "", {cls: 'builder'})
                    return
            if self.creep_registry.count_of_type(room, 'miner') < len(room.sources):  # 2
                if room.energyAvailable >= 550:
                    spawn.createCreep([WORK, WORK, WORK, WORK, MOVE], "", {cls: 'miner'})
                    return
            if self.creep_registry.count_of_type(room, 'hauler') < len(room.sources):  # TODO: ? 2
                if room.energyAvailable >= 550:
                    spawn.createCreep([WORK, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE, MOVE], "", {cls: 'hauler'})
                    return
            if self.creep_registry.count_of_type(room, 'upgrader') < 3:  # TODO: ? 3
                if room.energyAvailable >= 550:
                    spawn.createCreep([WORK, WORK, WORK, WORK, CARRY, MOVE, MOVE], "", {cls: 'upgrader'})
                    return
            # total of 7, so 0.2*7 = 1.4 CPU/tick - decisions

    def build(self):
        room = self.room
        if room.energyCapacityAvailable < 550:  # all extensions were not built yet
            #   S
            #   r
            # ere
            #eree
            spawn_pos = get_first_spawn(room).pos
            print('spawn_pos', room, spawn_pos.x, spawn_pos.y-2)
            room.getPositionAt(spawn_pos.x, spawn_pos.y-2).createConstructionSite(STRUCTURE_EXTENSION)
            room.getPositionAt(spawn_pos.x, spawn_pos.y-3).createConstructionSite(STRUCTURE_EXTENSION)
            room.getPositionAt(spawn_pos.x-1, spawn_pos.y-3).createConstructionSite(STRUCTURE_EXTENSION)
            room.getPositionAt(spawn_pos.x-2, spawn_pos.y-2).createConstructionSite(STRUCTURE_EXTENSION)
            room.getPositionAt(spawn_pos.x-3, spawn_pos.y-3).createConstructionSite(STRUCTURE_EXTENSION)

            room.getPositionAt(spawn_pos.x, spawn_pos.y-1).createConstructionSite(STRUCTURE_ROAD)
            room.getPositionAt(spawn_pos.x-1, spawn_pos.y-2).createConstructionSite(STRUCTURE_ROAD)
            room.getPositionAt(spawn_pos.x-2, spawn_pos.y-3).createConstructionSite(STRUCTURE_ROAD)
        pass  # TODO: build extensions, roads and containers automatically
        # extensions
        # shaped farms

        # roads (using self.creep_registry that has room stats and routes)

        # containers
        #target_container_count = self.room.source_count + 1
        #if target_container_count < len(self.room.sources):
        # for source in self.room.sources:
            # for each free space around source
            # sort the list by distance to controller
            # is container on that space already?
            #     continue
            # build a container

        # build a container next to controller
