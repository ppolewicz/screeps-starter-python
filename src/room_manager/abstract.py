from utils import get_first_spawn


class AbstractRoomManager:
    BUILD_SCHEDULE = 1  # try to build once every n ticks
    def __init__(self, room, creep_registry):
        self.room = room
        self.creep_registry = creep_registry

    def run(self):
        if self.creep_registry.count_of_type(self.room, 'harvester') == 0 and self.creep_registry.count_of_type(self.room, 'builder') == 0:
            # everyone died :|
            if self.room.energyAvailable < 550:
                # we either are in RCL1 anyway or we are RCL2 but nobody will fill spawn/extensions, lets just get someone to do that
                #return RoomManagerRCL1().spawn_creeps()
                if self.room.energyAvailable >= 250:  # wait until source is full (there are no extensions)
                    spawn = get_first_spawn(self.room)
                    spawn.createCreep([WORK, CARRY, MOVE, MOVE], "", {'cls': 'harvester'})
        self.spawn_creeps()
        if Game.time % self.BUILD_SCHEDULE == int(self.room.controller.id) % self.BUILD_SCHEDULE:
            print('running build planner')
            self.build()
        action_sets = []
        return action_sets

    def spawn_creeps(self):
        raise NotImplementedError

    def build(self):
        raise NotImplementedError
