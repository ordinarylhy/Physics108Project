class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.prev_error = 0
        self.integral = 0

    def update(self, current_value):
        error = self.setpoint - current_value
        self.integral += error
        derivative = error - self.prev_error

        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        self.prev_error = error
        return output

# Example usage
if __name__ == "__main__":
    # Set the PID constants
    Kp = 0.5
    Ki = 0.1
    Kd = 0.2

    # Set the desired temperature
    setpoint = 100  # Setpoint temperature in Celsius

    # Create PID controller object
    pid = PIDController(Kp, Ki, Kd, setpoint)

    # Simulated temperature
    current_temperature = 80  # Initial temperature

    # Simulate PID control loop
    for _ in range(100):
        # Get PID control output
        control_output = pid.update(current_temperature)

        # Simulate heater response (for example, add control output to current temperature)
        current_temperature += control_output

        # Print current temperature and control output
        print(f"Temperature: {current_temperature:.2f} C, Control Output: {control_output:.2f}")
