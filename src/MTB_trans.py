import can


def mechanical_angle_to_degree(mechanical_angle):
    """
    Trans Mechanical Angle to Degrees
    mechanical angle: 0~8191
    degree:0~360
    the formula is (mechanical_angle/8191)*360
    :param mechanical_angle: mechanical angle
    :return: angle in degrees
    """
    degree = round(mechanical_angle / 8191.0 * 360.0)
    return degree


def rotor_rpm_to_control_message(motor_number, rotor_rpm):
    """
    rotor rpm  to Control Data Value
    :param velocity: velocity in m/s
    :return:message for motor speed control
    """

    # Set Arbitration ID
    """
    MOTOR:
    motor's ID: 0~ 8
    For motor 1~4 msg.arbitration_id=0x200
    For motor 5~8 msg.arbitration_id=0x1FF
    """
    msg = can.Message(arbitration_id=0x200, data=[0, 0, 0, 0, 0, 0, 0, 0], is_extended_id=False)
    if 1 <= motor_number <= 4:
        msg.arbitration_id = 0x200
    else:
        msg.arbitration_id = 0x1FF

    current_value = rotor_rpm_to_current_value(rotor_rpm)
    msg = current_value_to_control_command(current_value, msg)
    return msg


def motor_data_to_decimal(high, low):
    """
    Total Data = High Data + Low Data
    High Data: 8bits
    Low Data: 8bits
    :param high: high_data
    :param low: low_data
    :return: their sum
    """
    result = high * (2 ** 8) + low
    return result


def wheel_velocity_to_rotor_rpm(velocity, wheel_radius=0.075):
    """
    Translate Velocity in m/s to rotor rpm
    velocity in m/s
    Assuming a wheel diameter of 150 mm, radius = 75 mm = 0.075 m
    circumference = 2 * PI * radius
    velocity = rpm of motor * circumference of wheel / 60.0
    :param velocity:
    :param wheel_radius:
    :return: rpm of rotor
    """
    pi = 3.1415926
    wheel_circumference = 2 * pi * wheel_radius
    motor_rpm = (velocity * 60.0) / wheel_circumference
    rotor_rpm = int(motor_rpm * 36.0)
    return rotor_rpm


def rotor_rpm_to_wheel_velocity(rotor_rpm, wheel_radius=0.075):
    """
    Translate  rotor rpm to Velocity in m/s
    velocity in m/s
    Assuming a wheel diameter of 150 mm, radius = 75 mm = 0.075 m
    circumference = 2 * PI * radius
    velocity = rpm of motor * circumference of wheel / 60.0
    :param rotor_rpm:
    :param wheel_radius:
    :return:
    """
    pi = 3.1415926
    wheel_circumference = 2 * pi * wheel_radius
    motor_rpm = rotor_rpm / 36.0
    velocity = motor_rpm * wheel_circumference / 60.0
    return velocity


def rotor_rpm_to_current_value(rotor_rpm):
    """
    Translate rpm of Rotor to Current Value
    This part ROUGHLY corresponds the magnitude of the current to the rotor speed
    MAX Rotor rpm = 18000
    Current range (-10000~10000)
    :param rotor_rpm:
    :return:
    """
    current = int(rotor_rpm / 18000 * 10000)
    return current


def current_value_to_control_command(current_value, message):
    """
    Convert current to hex list
    fill it with 0 so that the index of list is correct for high bit and low bit
    :param current_value:
    :param message:
    :return:
    """
    FLAG = 1
    current_hex_list = list(hex(current_value))
    if current_value < 0:
        current_hex_list = current_hex_list[1:]
        FLAG = -1
        while len(current_hex_list) < 6:
            current_hex_list.insert(2, '0')
        rotor_rpm_high = 255 + FLAG * int((current_hex_list[2] + current_hex_list[3]), 16)
        rotor_rpm_low = 255 + FLAG * int((current_hex_list[4] + current_hex_list[5]), 16)
    else:
        while len(current_hex_list) < 6:
            current_hex_list.insert(2, '0')
        rotor_rpm_high = int((current_hex_list[2] + current_hex_list[3]), 16)
        rotor_rpm_low = int((current_hex_list[4] + current_hex_list[5]), 16)

    message.data[0] = rotor_rpm_high
    message.data[1] = rotor_rpm_low
    return message
