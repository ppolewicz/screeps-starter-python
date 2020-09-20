from room_manager.rcl1 import RoomManagerRCL1
from room_manager.rcl2 import RoomManagerRCL2
from room_manager.rcl3 import RoomManagerRCL3


MANAGER_REGISTRY = [
    None,  # TODO: controlling rooms with level=0
    RoomManagerRCL1,
    RoomManagerRCL2,
    RoomManagerRCL2,  #TODO RoomManagerRCL3,
    RoomManagerRCL2,  #TODO RoomManagerRCL4,
    RoomManagerRCL2,  #TODO RoomManagerRCL5,
    RoomManagerRCL3,
    RoomManagerRCL3,
    RoomManagerRCL3,
]
