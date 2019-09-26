#include         //Servo library
 
 Servo servo_test;      //initialize a servo object for the connected servo  
                
 int angle = 0;    
 int potentio = A0;      // initialize the A0analog pin for potentiometer

 
 void setup() 
 { 
  servo_test.attach(9);   // attach the signal pin of servo to pin9 of arduino
 } 
 
 void loop() 
 { 
  angle = analogRead(potentio);            // reading the potentiometer value between 0 and 1023 
  angle = map(angle, 0, 1023, 0, 179);     // scaling the potentiometer value to angle value for servo between 0 and 180) 
  servo_test.write(angle);                   //command to rotate the servo to the specified angle 
  delay(5);             
 }  
