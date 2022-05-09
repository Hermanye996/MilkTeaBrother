class Pid(object):
    def __init__(self, min_value=-416, max_value=416, kp=0.6, ki=0.3, kd=0.5):
        self.max = max_value
        self.min = min_value

        self.Kp = kp
        self.Ki = ki
        self.Kd = kd

        self.previous_error = 0
        self.error = 0
        self.integral = 0
        self.derivative = 0

        # self.integral_value_limit = 0
        # self.integral_slope_limit = 0

    def pid_constrain(self, value, min_limit, max_limit):
        """
        Constrain PID Value
        PID value is constrained between Max and Min to prevent motor from error speed setting
        Max Motor RPM = 416 Min Motor RPM = -416 [from Official Support Document]
        :param value:PID Value unconstrained
        :return: PID Value Constrained
        """
        if value >= max_limit:
            value = max_limit
        elif value <= min_limit:
            value = min_limit

        return value

    def pid_calculate(self, target_value, current_value):
        """
        PID：
        C = Kp * ei + Ki * sum(ei)[1~N] + Kd *(ei - ei-1) /△t
        replace Kd/△t with new Kd
        error = target_value - current_value
        integral = integral + error
        derivative = error - previous_error

        :param target_value:
        :param current_value:
        :return:
        """
        self.error = target_value - current_value
        self.integral = self.integral + self.error
        """
        IF YOU WANT TO CONSTRAIN INTEGRAL, REPLACE ABOVE COMMAND WITH THIS PART 
        # Constrain Integral
        if abs(self.error) <= self.integral_slope_limit:
            self.integral = self.integral + self.error
            # limit excessive integral values
            self.integral = self.pid_constrain(self.integral, -self.integral_value_limit, self.integral_value_limit)
        else:  # ignore extreme integral changes
            self.integral = self.integral
        """
        self.derivative = self.error - self.previous_error

        # Clean integral if Robot Stopped
        if target_value == 0 and self.error == 0:
            self.integral = 0

        # Calculate PID Value and Constrain it
        pid_value = (self.Kp * self.error) + (self.Ki * self.integral) + (self.Kd * self.derivative)
        self.previous_error = self.error
        pid_value = self.pid_constrain(pid_value, self.min, self.max)
        return pid_value

    def pid_update_constants(self, constant_p, constant_i, constant_d):
        """
        Update Local PID constants from ROS Node about PID
        :param constant_p:
        :param constant_i:
        :param constant_d:
        :return:
        """
        self.Kp = constant_p
        self.Ki = constant_i
        self.Kd = constant_d
