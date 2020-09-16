class AbstractRoomManager:
    def __init__(self, room, creep_registry):
        self.room = room
        self.creep_registry = creep_registry

    def run(self):
        self.spawn_creeps()
        print('after spawn creeps', self.room)
        self.build()
        action_sets = []
        return action_sets

    def spawn_creeps(self):
        raise NotImplementedError

    def build(self):
        raise NotImplementedError
