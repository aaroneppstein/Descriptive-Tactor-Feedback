/*Main Experimental Code for Descriptive Tactor Feedback
adapted from the original failed python code :/ for firmata 
USED WITH DataAcquisition.py to connect to NI DAQ to record data and export to csv
Servo --> Digital PIN 3
*/

#include <Servo.h>


#define SERVO_PIN 3

Servo servo;

int pos;
int pos_0N = 0;       // Found from tester code
int pos_5N = 180/2;       // Found form tester code
int pos_10N = 180;      // Found from tester code

void setup() {
  Serial.begin(9600);

  servo.attach(SERVO_PIN);
  servo.write(pos_0N);
  delay(500);
  servo.write(pos_5N);
  delay(1000);
  
}

void loop() {
  char choice = Serial.read();
  if (choice == 'Y' || choice == 'y') {// Start if Python Serial Reader is ready
    delay(1000);
    for (pos = pos_5N; pos <= pos_10N; pos += 3)  {
      servo.write(pos);
      delay(25);                     
    }
    delay(500);
    for (pos = pos_10N; pos >= pos_0N; pos -= 3)  {
      servo.write(pos);

      delay(25);                       
    }
    delay(500);
    for (pos = pos_0N; pos <= pos_5N; pos += 3)  {
      servo.write(pos);

      delay(25);                   
    }
    delay(500);
    Serial.println("break");
  }
    

  else if (choice == 'N' || choice == 'n') {
    while(true){}                         // Infinite Tsukyumi
  }
}
  /*else {
    Serial.println("Invalid Response");
  }


  }*/
