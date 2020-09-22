from room_manager.rcl2 import RoomManagerRCL2
from utils import get_first_spawn


class RoomManagerRCL3(RoomManagerRCL2):
    def spawn_creeps(self):
        room = self.room
        spawn = get_first_spawn(room)
        if not spawn.spawning:
            if room.energyCapacityAvailable < 800:  # extensions were not built yet
                return RoomManagerRCL2(room).run()
            if len(self.creep_registry[room]['builder']) < 2:  # TODO: how many to keep, depending on the number of build sites
                if room.energyAvailable >= 550:
                    spawn.createCreep([WORK, WORK, WORK, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE, MOVE, MOVE], "", {memory: {cls: 'builder'}})
                    return
            if len(self.creep_registry[room]['miner']) < len(room.sources):  # 2
                if room.energyAvailable >= 800:
                    spawn.createCreep([WORK, WORK, WORK, WORK, WORK, WORK, WORK, MOVE, MOVE], "", {memory: {cls: 'miner'}})
                    return
            if len(self.creep_registry[room]['hauler']) < 1:
                if room.energyAvailable >= 800:
                    parts = [CARRY]*8
                    parts.extend([MOVE]*8)
                    spawn.createCreep(parts, "", {memory: {cls: 'hauler'}})
                    return
            if len(self.creep_registry[room]['upgrader']) < 2:  # TODO: ? 2
                if room.energyAvailable >= 800:
                    spawn.createCreep([WORK, WORK, WORK, WORK, WORK, WORK, WORK, CARRY, MOVE], "", {memory: {cls: 'upgrader'}})
                    return
            # total of 5, so 0.2*5 = 1.0 CPU/tick - decisions but even less bc miner will be idle half the time

    def run_build(self):
        return super().run_build()
        # TODO build a turret if there is none here yet
