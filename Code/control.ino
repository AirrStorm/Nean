#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

#define SERVO_FREQ 50 

char cmd;


#define SERVO_MIN 120
#define SERVO_MAX 520 

void setup() {
  Serial.begin(9600);

  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);

  delay(10);

  openHand(); 
}

void loop() {
  if (Serial.available()) {
    cmd = Serial.read();

    if (cmd == 'O') {
      openHand();
    }
    else if (cmd == 'C') {
      closeHand();
    }
  }
}

void openHand() {
  for (int i = 0; i < 5; i++) {
    pwm.setPWM(i, 0, SERVO_MIN);
  }
}

void closeHand() {
  for (int i = 0; i < 5; i++) {
    pwm.setPWM(i, 0, SERVO_MAX);
  }
}
