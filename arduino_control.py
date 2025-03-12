import serial


class ArduinoController:
    def __init__(self, port='COM3', baudrate=9600):
        self.arduino = serial.Serial(port, baudrate)

    def send_servo_positions(self, x, y):
        self.arduino.write(f'{x},{y}\n'.encode())

    def close(self):
        self.arduino.close()
