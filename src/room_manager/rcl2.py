from abstract import AbstractRoomManager


class RoomManagerRCL2(AbstractRoomManager):
    def spawn_creeps(self):
        if self.room.spawns[0].spawning:
            if self.room.energyCapacityAvailable < 550:  # extensions were not built yet
                return RoomManagerRCL1(self.room).run()  # keep RCL1 layout until they build up the extensions
            if len(creep_registry[room]['builder']) < 2:
                if self.room.energyAvailable >= 550:
                    self.spawns[0].createCreep([WORK, WORK, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE], "", {memory: {cls: 'builder'}})
                    return
            if len(creep_registry[room]['miner']) < len(room.sources):  # 2
                if self.room.energyAvailable >= 550:
                    self.spawns[0].createCreep([WORK, WORK, WORK, WORK, MOVE], "", {memory: {cls: 'miner'}})
                    return
            if len(creep_registry[room]['hauler']) < len(room.sources):  # TODO: ? 2
                if self.room.energyAvailable >= 550:
                    self.spawns[0].createCreep([WORK, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE, MOVE], "", {memory: {cls: 'hauler'}})
                    return
            if len(creep_registry[room]['upgrader']) < 3:  # TODO: ? 3
                if self.room.energyAvailable >= 550:
                    self.spawns[0].createCreep([WORK, WORK, WORK, WORK, CARRY, MOVE, MOVE], "", {memory: {cls: 'upgrader'}})
                    return
            # total of 7, so 0.2*7 = 1.4 CPU/tick - decisions

    def build(self):
        pass  # TODO: build extensions, roads and containers automatically
        # extensions

        # roads (using self.creep_registry that has room stats)

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
