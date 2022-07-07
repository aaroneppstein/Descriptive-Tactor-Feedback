/*Tester Code for Servo, Currrent Sensor and Load Cell read from NI DAQ
 * Also includes high voltage ping to sync Servo and Sensors
adapted from the original failed python code :/ for firmata 
Servo --> Digital PIN 3

*/

#include <Servo.h>

#define SERVO_PIN 3   
#define SYNC_PIN 5    // Sends PWM signal through AnalogWrite so has to be on a PWM pin   

Servo servo;

int pos = 0;

void setup() {
  Serial.begin(9600);

  servo.attach(SERVO_PIN);
  servo.write(0);
  
}

void loop() {
  char choice = Serial.read();
  
  if (choice == 'Y' || choice == 'y') {// Start if Python Serial Reader is ready
    /*delay(1000)
    analogWrite(SYNC_PIN,255)            // High Voltage Pin to Sync Data
    delay(2000)
    analogWrite(SYNC_PIN,0)*/
    /*int count = 0;
    while(true){
      loadcell.set_scale(calibration_factor);
      val = analogRead(POT_PIN);
      val = map(val,0,1023,0,180);
      servo.write(val);                       // Writing servo from Potentiometer
      Serial.print("Servo Position: ");
      Serial.print(val);
      Serial.print(" degrees ");
      Serial.print("Current Sensor: ");
      float volt_reading = bit_conv * analogRead(CURR_SENS_PIN);    //In mV
      float current_conv = (volt_reading - Vref) / sense;           //In A
      Serial.print(current_conv);
      Serial.print(" mA ");
      Serial.print("Scale: ");
      Serial.print(loadcell.get_units(), 1);
      Serial.print(" g");
      Serial.println();
      count += 1;
      delay(100);           // Waits for 150 ms
      /*if (count > 100){
        Serial.println("break");
        break;
      }
    }*/
  /*
  else if (choice == 'N' || choice == 'n') {
    while(true){}                         // Infinite Tsukyumi
  }*/
  /*else {
    Serial.println("Invalid Response");
  }*/


  //}
// 174 degrees found to be initial parameter of 10 N of force
  delay(1500);
  //analogWrite(SYNC_PIN,200);
  //delay(2000);
  //analogWrite(SYNC_PIN,0);
  for (pos = 0; pos <= 180; pos += 3) { // goes from 0 degrees to 180 degrees
    // in steps of 3 degrees
    servo.write(pos);                 // tell servo to go to position in variable 'pos'

    Serial.print(pos);
    Serial.println();
    
    delay(25);     
    //delay(1); 
                          
  }

  delay(1000);     // Holding in position for 1 second 
  
  for (pos = 180; pos >= 0; pos -= 3) { // goes from 0 degrees to 180 degrees
    // in steps of 3 degree
    servo.write(pos);                 // tell servo to go to position in variable 'pos'
    
    Serial.print(pos);

    Serial.println();

    delay(25);
    //delay(1);                        
  }

  delay(1000);

Serial.println("break");
}
}
