#include <Servo.h>

Servo servoX;
Servo servoY;

void setup() {
    Serial.begin(9600);
    servoX.attach(9);
    servoY.attach(10);

    servoX.write(90);
    servoY.write(135);
    delay(1000);
}

void loop() {
    if (Serial.available()) {
        String data = Serial.readStringUntil('\n');
        int commaIndex = data.indexOf(',');

        if (commaIndex != -1) {
            int x_angle = data.substring(0, commaIndex).toInt();
            int y_angle = data.substring(commaIndex + 1).toInt();

            servoX.write(x_angle);
            servoY.write(y_angle);
        }
    }
}