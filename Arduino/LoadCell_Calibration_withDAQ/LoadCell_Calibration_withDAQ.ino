// To be used with LoadCellCalibration_Acquisition.py to find values of voltages to weights

char choice;
void setup(){
  Serial.begin(9600);
  delay(1000);
  Serial.println("Calibration Testing shall comence");
  Serial.println("Please test weights in following set: No weight, 100g, 200g, 500g, 1000g, 1400g");
  delay(500);
}
 void loop(){
  
  choice = Serial.read();
  if (choice == 'Y' || choice == 'y') {// Start if Python Serial Reader is ready
    Serial.println("Collecting Load Cell Voltages");
    delay(5000);
    Serial.println("break");
  }
  if (choice == 'N' || choice == 'n') {
    while(true){}
  }
 

}
