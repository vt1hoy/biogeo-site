from pymavlink import mavutil
import time

# подключение к автопилоту (SITL)
master = mavutil.mavlink_connection("tcp:127.0.0.1:5760")

print("Waiting for heartbeat...")
master.wait_heartbeat()
print("Connected")

# перевод в GUIDED
mode_id = master.mode_mapping()['GUIDED']
master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mode_id
)

# арминг
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 0, 0, 0, 0, 0, 0
)

print("Armed")

# отправка точки (пример)
lat = int(14.7560 * 1e7)
lon = int(-17.5150 * 1e7)
alt = 20

master.mav.set_position_target_global_int_send(
    0,
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
    int(0b110111111000),
    lat,
    lon,
    alt,
    0, 0, 0,
    0, 0, 0,
    0, 0
)

print("Waypoint sent")

# чтение телеметрии
for _ in range(10):
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    print(msg)