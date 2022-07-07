#include <Servo.h>
Servo myservo;

int pot = 1;
int val;

void setup() {

myservo.attach(3);

}

void loop() {
  val = analogRead(pot);
  val = map(val,0,1023,0,180);
  myservo.write(val);       // Writing servo from Potentiometer
  delay(75);                // Waits for 75 ms
}
