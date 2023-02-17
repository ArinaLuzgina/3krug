#include <ros.h>
#include <std_msgs/Float32MultiArray.h>
#include <std_msgs/Int32MultiArray.h>

class NewHardware : public ArduinoHardware {
public:
  NewHardware()
    : ArduinoHardware(&Serial, 115200){};
};
ros::NodeHandle_<NewHardware> nh;

int speedPins[3] = { 5, 6, 8 };
int directionPins[3] = { 4, 7, 9 };

float speedValues[3] = { 0.0, 0.0, 0.0 };
int directionValues[3]{ 0, 0, 0 };

// pins for the encoder inputs
#define RH_ENCODER_A 11
#define RH_ENCODER_B 3
#define LH_ENCODER_A 10
#define LH_ENCODER_B 2
#define FH_ENCODER_A 12
#define FH_ENCODER_B 19



// variables to store the number of encoder pulses
// for each motor
long leftCount = 0;
long rightCount = 0;
long leftCountPrev = 0;
long rightCountPrev = 0;
long frontCount = 0;
long frontCountPrev = 0;

// Use it to make a delay... without delay() function!
unsigned long previousMillis = 0;  // If you use 0 then you will take the first value after interval.
long interval = 100;               //100;             // interval at which to rea
unsigned long currentMillis;
unsigned long delta;

//Useful Variables
float DistA_m, DistB_m, DistC_m;


void messageCb(const std_msgs::Float32MultiArray &msg) {

  for (size_t i = 0; i != 6; i += 2) {
    if (msg.data[i + 1] == 1.0) {
      speedValues[i / 2] = msg.data[i];
      directionValues[i / 2] = 1;
    } else {
      speedValues[i / 2] = -msg.data[i];
      directionValues[i / 2] = 0;
    }
  }


  for (int i = 0; i != 3; ++i) {
    if (speedValues[i] > 0.2) { speedValues[i] = 0.15; }
    analogWrite(speedPins[i], speedValues[i] * 255);
    if (directionValues[i] == 1.0) {
      digitalWrite(directionPins[i], HIGH);
    } else {
      digitalWrite(directionPins[i], LOW);
    }
  }
}
ros::Subscriber<std_msgs::Float32MultiArray> sub("speed_publisher", &messageCb);

std_msgs::Int32MultiArray msg;
ros::Publisher ticks("ticks", &msg);

void setup() {
  // encoder pins
  pinMode(LH_ENCODER_A, INPUT);
  pinMode(LH_ENCODER_B, INPUT);
  pinMode(RH_ENCODER_A, INPUT);
  pinMode(RH_ENCODER_B, INPUT);
  pinMode(FH_ENCODER_A, INPUT);
  pinMode(FH_ENCODER_B, INPUT);
  // initialize hardware interrupts
  attachInterrupt(0, leftEncoderEvent, CHANGE);   // pin 2 Interrupt   -- это место стоит исправить используя  digitalPinToInterrupt(pin)
  attachInterrupt(1, rightEncoderEvent, CHANGE);  // pin 3 Interrupt
  attachInterrupt(4, frontEncoderEvent, CHANGE);


  msg.data_length = 4;



  for (int i = 0; i < 3; ++i) {
    pinMode(speedPins[i], OUTPUT);
    pinMode(directionPins[i], OUTPUT);
  }


  nh.initNode();
  nh.advertise(ticks);
  nh.subscribe(sub);
  previousMillis = millis();
}


void loop() {
  currentMillis = millis();
  if (currentMillis - previousMillis > interval) {
    DistA_m = leftCount - leftCountPrev;    //*WheelParam;
    DistB_m = rightCount - rightCountPrev;  //*WheelParam;
    DistC_m = frontCount - frontCountPrev;
    delta = currentMillis - previousMillis;
    leftCountPrev = leftCount;
    rightCountPrev = rightCount;
    frontCountPrev = frontCount;
    msg.data[0] = DistA_m;
    msg.data[1] = DistB_m;
    msg.data[2] = DistC_m;
    msg.data[3] = delta;

    ticks.publish(&msg);
    previousMillis = currentMillis;
    nh.spinOnce();
  }

  delay(10);
}

// encoder event for the interrupt call
void leftEncoderEvent() {
  if (digitalRead(LH_ENCODER_A) == HIGH) {
    if (digitalRead(LH_ENCODER_B) == LOW) {
      leftCount++;
    } else {
      leftCount--;
    }
  } else {
    if (digitalRead(LH_ENCODER_B) == LOW) {
      leftCount--;
    } else {
      leftCount++;
    }
  }
}

// encoder event for the interrupt call
void rightEncoderEvent() {
  if (digitalRead(RH_ENCODER_A) == HIGH) {
    if (digitalRead(RH_ENCODER_B) == LOW) {
      rightCount++;
    } else {
      rightCount--;
    }
  } else {
    if (digitalRead(RH_ENCODER_B) == LOW) {
      rightCount--;
    } else {
      rightCount++;
    }
  }
}

void frontEncoderEvent() {
  if (digitalRead(FH_ENCODER_A) == HIGH) {
    if (digitalRead(FH_ENCODER_B) == LOW) {
      frontCount++;
    } else {
      frontCount--;
    }
  } else {
    if (digitalRead(FH_ENCODER_B) == LOW) {
      frontCount--;
    } else {
      frontCount++;
    }
  }
}
