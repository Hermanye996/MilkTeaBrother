#!/usr/bin/env python3
# -- coding: utf-8 --
import can
import os
import MTB_trans
import time


def can_setup(bustype='socketcan', channel='can0', bitrate=1000000):
    """
    Set Up CAN with Cantools
    OS code: 0 Success
    OS code: 1 Operation not permitted
    :return:None
    """
    # Set CAN bus
    bus = can.Bus(bustype=bustype, channel=channel, bitrate=bitrate)
    if os.system("sudo ip link set can0 up type can bitrate 1000000") == 1:
        print("ERROR!")
    elif os.system("sudo ip link set can0 up type can bitrate 1000000") == 0:
        print("can0 status: ON")
    return bus


def can_stop():
    """
    Stop CAN with Cantools
    :return:None
    """
    if os.system("sudo ip link set can0 down") == 1:
        print("ERROR!")
    elif os.system("sudo ip link set can0 down") == 0:
        print("can0 status: OFF")


def receive_motor_data(can_msg):
    """
    Receive Motor Data from C610 Motor Governor and Translate Hex Data to Decimal Data
    :param can_msg:
    :return:
    """

    # Fetch Arbitration ID of Device
    """
    motors' arbitration id: 0x20* in hex
    Example: id=1 motor1's arbitration id is 0x201
    """
    device_id_hex = hex(can_msg.arbitration_id)

    # Calculate Angle in Degrees
    """
    DATA[0] : rotor mechanical angle_high
    DATA[1] : rotor mechanical angle_low
    data read from CAN bus is automatically translated into decimal type
    total mechanical angle in decimal = mechanical angle_high * (2 ** 8) + mechanical angle_low
    """
    mechanical_angle_high = can_msg.data[0]
    mechanical_angle_low = can_msg.data[1]
    mechanical_angle = MTB_trans.motor_data_to_decimal(mechanical_angle_high, mechanical_angle_low)
    angle = MTB_trans.mechanical_angle_to_degree(mechanical_angle)

    # Calculate Motor Rotating Speed
    """
    DATA[2] : speed_high of rotor in rpm
    DATA[3] : speed_low of rotor in rpm
    when speed is negative,the speed value should be speed-65536
    16 ** 4 = 65536
    reduction ratio of M2006 motor is 36:1
    rotating speed of motor =round( rotating speed of rotor / 36.0)
    """
    rotor_rpm_high = can_msg.data[2]
    rotor_rpm_low = can_msg.data[3]
    rotor_rpm = MTB_trans.motor_data_to_decimal(rotor_rpm_high, rotor_rpm_low)

    if rotor_rpm > 32768:
        rotor_rpm = rotor_rpm - 65536
    # Print Results
    """
    print("Device: " + str(device_id_hex) + " Current Angle: " + "\t" + str(
        angle) + "\t" + "Motor Rotating Speed: " + "\t" + str(motor_speed) + " rpm")
    """
    return rotor_rpm


def send_motor_control_command(msg, bus):
    bus.send_periodic(msg, 0.001, 0.01)


def receive_can_information(bus):
    for msg in bus:
        receive_motor_data(msg)
    time.sleep(200)
