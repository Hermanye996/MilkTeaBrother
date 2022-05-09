#!/usr/bin/env python3
# -- coding: utf-8 --
import MTB_can
import MTB_pid
import MTB_trans
import MTB_config as config


if __name__ == '__main__':
    bus = MTB_can.can_setup()
    motor1 = 1
    motor1_pid = MTB_pid.Pid(config.pid_min, config.pid_max, config.pid_p, config.pid_i, config.pid_d)

    pid_count = 0
    for msg in bus:
        pid_count = pid_count + 1
        if pid_count == int(1000 / config.pid_frequency):
            pid_count = 0
            current_rotor_rpm_pre = MTB_can.receive_motor_data(msg)
            if current_rotor_rpm_pre != 0:
                # 因为接受的信息里有一部分是0的，因此需要过滤避免影响pid，暂时没有好办法
                current_rotor_rpm = current_rotor_rpm_pre
                print("currentVel=" + str(current_rotor_rpm))

                pid_rpm_value = motor1_pid.pid_calculate(config.target_rotor_rpm, current_rotor_rpm)
                print("pid_rpm= " + str(pid_rpm_value))
                msg = MTB_trans.rotor_rpm_to_control_message(motor1, pid_rpm_value)
                MTB_can.send_motor_control_command(msg, bus)

