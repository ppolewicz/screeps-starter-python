from utils import get_first_spawn
from room_manager.abstract import AbstractRoomManager
from room_manager.rcl1 import RoomManagerRCL1


class RoomManagerRCL2(AbstractRoomManager):
    def spawn_creeps(self):
        room = self.room
        spawn = get_first_spawn(room)
        if not spawn.spawning:
            if room.energyCapacityAvailable < 550:  # extensions were not built yet
                return self.spawn_creeps_in_transition_period()
            elif self.creep_registry.count_of_type(room, 'builder') < 4:  # TODO: all like this
                if room.energyAvailable >= 550:
                    spawn.createCreep([WORK, WORK, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE], "", {cls: 'builder'})
            elif self.creep_registry.count_of_type(room, 'miner') < len(room.sources):  # 2
                if room.energyAvailable >= 550:
                    spawn.createCreep([WORK, WORK, WORK, WORK, MOVE], "", {cls: 'miner'})
            elif self.creep_registry.count_of_type(room, 'hauler') < len(room.sources):  # TODO: ? 2
                if room.energyAvailable >= 550:
                    spawn.createCreep([WORK, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE, MOVE], "", {cls: 'hauler'})
            elif self.creep_registry.count_of_type(room, 'upgrader') < 3:  # TODO: ? 3
                if room.energyAvailable >= 550:
                    spawn.createCreep([WORK, WORK, WORK, WORK, CARRY, MOVE, MOVE], "", {cls: 'upgrader'})
            # total of 7, so 0.2*7 = 1.4 CPU/tick - decisions

    def spawn_creeps_in_transition_period(self):
        if room.energyCapacityAvailable == 300:
            return RoomManagerRCL1(room, self.creep_registry).spawn_creeps()  # keep RCL1 layout until they build up the extensions
        elif room.energyCapacityAvailable == 350:
            if self.creep_registry.count_of_type(room, 'harvester') < RoomManagerRCL1.MAX_HARVESTERS:  # keep spawning them, why not
                if room.energyAvailable >= 350:
                    spawn.createCreep([WORK, CARRY, CARRY, MOVE, MOVE, MOVE], "", {'cls': 'harvester'})
        elif room.energyCapacityAvailable == 450:
            if self.creep_registry.count_of_type(room, 'harvester') < RoomManagerRCL1.MAX_HARVESTERS:  # keep spawning them, why not
                if room.energyAvailable >= 450:
                    spawn.createCreep([WORK, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE], "", {'cls': 'harvester'})
        elif room.energyCapacityAvailable == 500:
            if self.creep_registry.count_of_type(room, 'harvester') < RoomManagerRCL1.MAX_HARVESTERS:  # keep spawning them, why not
                if room.energyAvailable >= 500:
                    spawn.createCreep([WORK, WORK, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE], "", {'cls': 'harvester'})

    def build(self):
        room = self.room
        if room.energyCapacityAvailable < 550:  # all extensions were not built yet
            #eree
            # ere
            #   r
            #   S
            spawn_pos = get_first_spawn(room).pos
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
