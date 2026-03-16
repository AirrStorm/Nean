#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN 110
#define SERVOMAX 640
#define SERVO_FREQ 50

// Finger channels
#define INDEX 0
#define MIDDLE 1
#define RING 2
#define PINKY 3

uint16_t angleToPulse(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}

// Map 'open'/'closed' to servo angle based on finger
int fingerAngle(String finger, String state) {
  if (finger == "index" || finger == "middle") {
    return (state == "closed") ? 0 : 130; // bent = 0, straight = 130
  } else if (finger == "ring" || finger == "pinky") {
    return (state == "closed") ? 130 : 0; // bent = 130, straight = 0
  }
  return 0;
}

void setup() {
  Serial.begin(115200);
  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);
  delay(10);

  // INITIAL POSITIONS: all straight
  pwm.setPWM(INDEX, 0, angleToPulse(130));
  pwm.setPWM(MIDDLE, 0, angleToPulse(130));
  pwm.setPWM(RING, 0, angleToPulse(0));
  pwm.setPWM(PINKY, 0, angleToPulse(0));
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n'); // read one line

    String fingers[] = {"index", "middle", "ring", "pinky"};
    int channels[] = {INDEX, MIDDLE, RING, PINKY};

    for (int i = 0; i < 4; i++) {
      int sep1 = data.indexOf(fingers[i] + ":");
      if (sep1 >= 0) {
        int sep2 = data.indexOf(",", sep1);
        String value = data.substring(sep1 + fingers[i].length() + 1,
                                     sep2 >= 0 ? sep2 : data.length());
        value.trim(); // remove any extra whitespace
        pwm.setPWM(channels[i], 0, angleToPulse(fingerAngle(fingers[i], value)));
      }
    }
  }
}