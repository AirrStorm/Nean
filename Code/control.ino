#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN 110
#define SERVOMAX 640
#define SERVO_FREQ 50

// Channels
#define THUMB  0
#define INDEX  1
#define MIDDLE 2
#define RING   3
#define PINKY  4

uint16_t angleToPulse(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}

void setup() {
  Serial.begin(115200);
  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);
  delay(10);

  // Start all fingers open
  pwm.setPWM(THUMB,  0, angleToPulse(0));
  pwm.setPWM(INDEX,  0, angleToPulse(0));
  pwm.setPWM(MIDDLE, 0, angleToPulse(0));
  pwm.setPWM(RING,   0, angleToPulse(130));
  pwm.setPWM(PINKY,  0, angleToPulse(130));
}

void loop() {
  if (Serial.available()) {

    String data = Serial.readStringUntil('\n');

    // -------------------
    // THUMB
    // -------------------
    if (data.indexOf("thumb:closed") >= 0) {
      pwm.setPWM(THUMB, 0, angleToPulse(130));
    }
    if (data.indexOf("thumb:open") >= 0) {
      pwm.setPWM(THUMB, 0, angleToPulse(0));
    }

    // -------------------
    // INDEX (uses swapped logic)
    // -------------------
    if (data.indexOf("index:closed") >= 0) {
      pwm.setPWM(INDEX, 0, angleToPulse(130));
    }
    if (data.indexOf("index:open") >= 0) {
      pwm.setPWM(INDEX, 0, angleToPulse(0));
    }

    // -------------------
    // MIDDLE (same as index)
    // -------------------
    if (data.indexOf("middle:closed") >= 0) {
      pwm.setPWM(MIDDLE, 0, angleToPulse(130));
    }
    if (data.indexOf("middle:open") >= 0) {
      pwm.setPWM(MIDDLE, 0, angleToPulse(0));
    }

    // -------------------
    // RING (opposite logic)
    // -------------------
    if (data.indexOf("ring:closed") >= 0) {
      pwm.setPWM(RING, 0, angleToPulse(0));
    }
    if (data.indexOf("ring:open") >= 0) {
      pwm.setPWM(RING, 0, angleToPulse(130));
    }

    // -------------------
    // PINKY (same as ring)
    // -------------------
    if (data.indexOf("pinky:closed") >= 0) {
      pwm.setPWM(PINKY, 0, angleToPulse(0));
    }
    if (data.indexOf("pinky:open") >= 0) {
      pwm.setPWM(PINKY, 0, angleToPulse(130));
    }
  }
}
