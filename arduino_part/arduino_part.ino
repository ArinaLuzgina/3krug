#include <ros.h>
#include <std_msgs/Float32MultiArray.h>
#include <std_msgs/Float32.h>

class NewHardware : public ArduinoHardware
{
  public:
  NewHardware():ArduinoHardware(&Serial, 115200){};
};
ros::NodeHandle_<NewHardware>  nh;


int speedPins[3] ={5, 6, 8};
int directionPins[3] = {4, 7, 9};

float speedValues[3] = {0.0, 0.0, 0.0};
int directionValues[3] {0, 0, 0};

std_msgs::Float32 str_msg;
ros::Publisher chatter("chatter", &str_msg);

void messageCb(const std_msgs::Float32MultiArray& msg){

    for(size_t i = 0; i != 6; i += 2){
      if(msg.data[i + 1] == 1.0){
        speedValues[i / 2] = msg.data[i];
        directionValues[i / 2] = 1;
      }
      else{
        speedValues[i / 2] = msg.data[i];
        directionValues[i / 2] = 0;
      }
      }
    
      
      for(int i = 0; i != 3; ++i){
        float maxValue = max(speedValues[0], speedValues[1]);
        maxValue = max(maxValue, speedValues[2]);
        analogWrite(speedPins[i], speedValues[i] / maxValue * 254);
        str_msg.data = speedValues[i] / maxValue * 254;
        chatter.publish(&str_msg);
        if(directionValues[i] == 1.0){
         digitalWrite(directionPins[i], HIGH); 
        }
        else{
          digitalWrite(directionPins[i], LOW);
        }
      }

     

}
ros::Subscriber<std_msgs::Float32MultiArray> sub("speed_publisher", &messageCb );


void setup() {
  for(int i = 0; i < 3; ++i){
    pinMode(speedPins[i], OUTPUT);
    pinMode(directionPins[i], OUTPUT);
  }

  nh.initNode();
  nh.subscribe(sub);
  nh.advertise(chatter);
 }

void loop() {

  nh.spinOnce();
  delay(1);

}
