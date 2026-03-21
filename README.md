# Nean
A custom made 3d printed tendon driven robotic hand made to learn more about mechanical designs and a bit of biology. It is loosely based on how the human hand actually works. It uses strings to pull the fingers open and close similar to real muscles in the palm. It uses a python script to read finger positions and controls the movement of the hand.

---

## 🧰 Parts Needed

- Arduino Uno
- 2 18650 li-ion batteries
- Switch
- 16-Channel 12-bit PWM/Servo Driver - PCA9685
- 5 MG90s servos
- Elastic Cord
- Fishing Line
- Buck Converter LM2596S
  
---

## Wiring
Here is a preview of the wiring:

![Wiring Preview](Wiring%20Diagram/Nean.png)

You can find the wiring diagram here:
```
Nean/
├── Wiring Diagram/
   └── Nean.png
```

---

## 3d Models
You can find the STEP files here:

```
Nean/
└──  STEP files/
```
And the STL files here:

```
Nean/
└──  STL files/
```
When 3d printing the models, for the fingers, only 3d print the parts that have "phalanx" at the end, the ones with "Finger" at the end are the full models of the fingers if you want to make changes. And for the arm models, print everything except the "Arm.step" file, which is the full 3d model of the arm if you want to make changes.

Here is a preview of the 3d model:

<img width="408" height="628" alt="image" src="https://github.com/user-attachments/assets/3b409a60-a53f-45c3-a59e-4063af831018" />

--- 

## Firmware

You can find the firmware files at:
```
Nean/
└──  Code/
```
It consist of a python file that runs on yout computer and one you upload to the ESP32.
The control system is simple, the python file checks if you hand is open or closed an sends it to the ESP32 via serial communication (I plan to change to wifi later)

---

## Disclaimer
The project is not done, I am yet to test everything together


