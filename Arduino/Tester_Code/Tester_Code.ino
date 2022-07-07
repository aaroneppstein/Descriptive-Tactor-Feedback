/*Tester Code for Servo, Current Sensor, and Load Cell all in one 
adapted from the original failed python code :/ for firmata 
Load Cell --> Calibrated in LoadCell_Calibration.ino -> Digital PIN 4 PIN 5
Servo --> Digital PIN 3
Current Sensor --> Analog PIN 0
Potentiometer --> Analog PIN 5
*/

#include "HX711_mod.h" //This library was modified but the original can be obtained here http://librarymanager/All#Avia_HX711
#include <Servo.h>


#define CURR_SENS_PIN 0
#define POT_PIN 5
#define SERVO_PIN 3
#define LOADCELL_DOUT_PIN  4      
#define LOADCELL_SCK_PIN  5       

HX711 loadcell;
Servo servo;

int pos = 0;
int val;
int CS_val;
//int count = 0;
//float calibration_factor = 443;      //Platform ~ From LoadCell_calibration.ino 
float calibration_factor = 441;      // Platform + Syndaver ~ From LoadCell_calibration.ino
float sense = 400;                   //Base Sensitivity of 400 mV/A from Datasheet
float Vref;                           //Output voltage with no current from DataSheet in mV
float bit_conv = 5000/1024;          //Converting Analog 1024 bit to 5000 mV
float sensorValue;
// int avgSamples = 200;
int calibrate_curr_sens = 10000;

void setup() {
  Serial.begin(9600);

  servo.attach(SERVO_PIN);
  servo.write(0);
  loadcell.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  loadcell.set_scale();
  loadcell.tare();  //Reset the scale to 0
  //Serial.println("Scale --> Tared and Ready");

  //Current Sensor Calibration
  for (int i = 0; i < calibrate_curr_sens; i++){
    sensorValue += analogRead(CURR_SENS_PIN);
        delay(.25);                      // 40 kHz 
  }
  float sensorRef = sensorValue/ calibrate_curr_sens;
  Vref = bit_conv * sensorRef;
  //Serial.println(Vref);
  
  
}

void loop() {
  char choice = Serial.read();
  
  if (choice == 'Y' || choice == 'y') {// Start if Python Serial Reader is ready
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
  /*int pos_vals[361];
  float CS_vals[361];
  float LC_vals[361];*/
  loadcell.set_scale(calibration_factor);
  for (pos = 0; pos <= 174; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 3 degrees
    servo.write(pos);                 // tell servo to go to position in variable 'pos'
    /*for (int i = 0; i < avgSamples; i++){     //Averaging Samples for cleaner signal
      sensorValue += analogRead(CURR_SENS_PIN);
      delay(.25);                     // 40 kHz 
    }
    sensorValue = sensorValue/ avgSamples; */
    sensorValue = analogRead(CURR_SENS_PIN);
    float volt_reading = bit_conv * sensorValue;    //In mV
    float current_conv = ((volt_reading - Vref) / sense) * 1000;           //In mA
    //long LoadCell_grams = (loadcell.get_units(),1);
    
    //Serial.print("Servo Position: ");
    Serial.print(pos);
    Serial.print(" ");
    //Serial.print(" degrees ");
    //Serial.print("Current Sensor: "); 
    //Serial.print(sensorValue);
    
    //Serial.println(volt_reading);
    //Serial.print(" ");
    
    Serial.print(current_conv);
    Serial.print(" ");
    //Serial.print(" mA ");
    
    //Serial.print("Scale: ");

    //Serial.print(loadcell.get_units(), 1);
    
    
    //Serial.print(" g");
    Serial.println();

    //pos_vals[pos] = pos;
    //CS_vals[pos] = current_conv;
    //LC_vals[pos] = LoadCell_grams;
    
    
    delay(.25);        //Max data rate of HX711 80 Hz wanna sample at 2 times that (Niquist Theorem)
    //delay(1); 
                          
  }
  for (pos = 174; pos >= 0; pos -= 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    servo.write(pos);                 // tell servo to go to position in variable 'pos'
    /*for (int i = 0; i < avgSamples; i++){     //Averaging Samples for cleaner signal
      sensorValue += analogRead(CURR_SENS_PIN);
      delay(.25);                      // 40 kHz 
    }
    sensorValue = sensorValue/ avgSamples;*/
    sensorValue = analogRead(CURR_SENS_PIN);
    float volt_reading = bit_conv * sensorValue;    //In mV
    float current_conv = ((volt_reading - Vref) / sense) * 1000;           //In mA
    //long LoadCell_grams = (loadcell.get_units(),1);
    
    //Serial.print("Servo Position: ");
    Serial.print(pos);
    Serial.print(" ");
    //Serial.print(" degrees ");
    //Serial.print("Current Sensor: "); 
    //Serial.print(sensorValue);
    
    //Serial.println(volt_reading);
    //Serial.print(" ");
    
    Serial.print(current_conv);
    Serial.print(" ");
    //Serial.print(" mA ");
    
    //Serial.print("Scale: ");
    //Serial.print(loadcell.get_units(), 1);
    
    //Serial.print(" g");
    Serial.println();

    //pos_vals[pos] = pos;
    //CS_vals[pos] = current_conv;
    //LC_vals[pos] = LoadCell_grams;
    
    
    delay(.25);
    //delay(1);                        
  }
  /*for (int i = 0; i <= 361; i += 1){
    Serial.println(pos_vals[i]);
    Serial.println(CS_vals[i]);
    //Serial.println(LC_vals[i]);
    
  }*/
  Serial.println("break");
}
}
