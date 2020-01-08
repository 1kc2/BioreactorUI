#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void setup() {
    Serial.begin(9600);
}

void loop() {
    //Serial.println("no data");
  // put your main code here, to run repeatedly: 
     if (Serial.available() > 0 && Serial.read() == '<')
     {
      //  Serial.println("data available");
        char input[25];
        int charsRead = Serial.readBytesUntil('>', input, 25);
        input[charsRead] = '\0';
        char* ptr = strtok(input, ",");
        char* ptr2 = strtok(NULL, ",");
        Serial.print(ptr);
        Serial.print(" ");
        Serial.println(ptr2);
        double val = atof(ptr2);
        //Serial.println(val);
     }
     delay(200);
}

