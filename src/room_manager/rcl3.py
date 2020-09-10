from rcl2 import RoomManagerRCL2


class RoomManagerRCL3(RoomManagerRCL2):
    def spawn_creeps(self):
        if room.spawns[0].spawning:
            if room.energyCapacityAvailable < 800:  # extensions were not built yet
                return RoomManagerRCL2(room).run()
            if len(creep_registry[room]['builder']) < 2:  # TODO: how many to keep, depending on the number of build sites
                if self.room.energyAvailable >= 550:
                    self.spawns[0].createCreep([WORK, WORK, WORK, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE, MOVE, MOVE], "", {memory: {cls: 'builder'}})
                    return
            if len(creep_registry[room]['miner']) < len(room.sources):  # 2
                if self.spawns[0].room.energyAvailable >= 800:
                    self.spawns[0].createCreep([WORK, WORK, WORK, WORK, WORK, WORK, WORK, MOVE, MOVE], "", {memory: {cls: 'miner'}})
                    return
            if len(creep_registry[room]['hauler']) < 1:
                if self.spawns[0].room.energyAvailable >= 800:
                    parts = [CARRY]*8
                    parts.extend([MOVE]*8)
                    self.spawns[0].createCreep(parts, "", {memory: {cls: 'hauler'}})
                    return
            if len(creep_registry[room]['upgrader']) < 2:  # TODO: ? 2
                if self.spawns[0].room.energyAvailable >= 800:
                    self.spawns[0].createCreep([WORK, WORK, WORK, WORK, WORK, WORK, WORK, CARRY, MOVE], "", {memory: {cls: 'upgrader'}})
                    return
            # total of 5, so 0.2*5 = 1.0 CPU/tick - decisions but even less bc miner will be idle half the time

    def build(self):
        return super().build()
        # TODO build a turret if there is none here yet
