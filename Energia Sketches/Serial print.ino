/*
  Blink
  The basic Energia example.
  Turns on an LED on for one second, then off for one second, repeatedly.
  Change the LED define to blink other LEDs.

  Hardware Required:
  * LaunchPad with an LED

  This example code is in the public domain.
*/

// most launchpads have a red LED
#define LED YELLOW_LED

//see pins_energia.h for more LED definitions
//#define LED GREEN_LED

// the setup routine runs once when you press reset:
void setup() {
  // initialize the digital pin as an output.
    Serial.begin(9600);
  pinMode(LED, OUTPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  //digitalWrite(LED, HIGH);   // turn the LED on (HIGH is the voltage level)
  //float foo = 7;
  float foo = random(2, 8);
  //float foo1 = 32;
  float foo1 = random(26, 39);
  //float foo2 = 1500;
  float foo2 = random(1400, 1600);
  Serial.print("<pH,");
  Serial.print(foo);
  Serial.println(">");
  delay(100);
  Serial.print("<temperature,");
  Serial.print(foo1);
  Serial.println(">");
  delay(100);
  Serial.print("<speed,");
  Serial.print(foo2);
  Serial.println(">");
  delay(100);               // wait for a second
  //digitalWrite(LED, LOW);    // turn the LED off by making the voltage LOW
 // delay(500);               // wait for a second
}
