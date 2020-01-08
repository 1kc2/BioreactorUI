int pHpin=A1;
        int acid=39;
        int base=40;
     float   F=9.6485309e4;
     float R=8.314510;
     int T=290;
     float V_supply=0.82;
     float C=2.302585;
     float a;
     float b;
     int ph_entered = 0;
     char str_pHmin[24];
     char str_pHmax[24];
     float pHmin;
     float pHmax;
#include <stdio.h>



void setup() {

pinMode(acid, OUTPUT);
pinMode(base, OUTPUT);
pinMode(pHpin, INPUT);
Serial.begin(9600);




}


void start() {
    int count = 1;
    Serial.println("please input minimum value of pH");
    str_pHmin[0] = Serial.read();
    //delay(5000);
    if (Serial.available() >  0) {
        while (Serial.available() > 0) {
            str_pHmin[count] = Serial.read();
            count++;
        }
    }
    str_pHmin[count] = '\0';
    count = 1;
    Serial.println("please input maximum value of pH");
    str_pHmax[0] = Serial.read();
    if (Serial.available() >  0)
    {while (Serial.available() > 0)
    {str_pHmax[count] = Serial.read();
     count++;}
    }
    str_pHmax[count] = '\0';

}

void loop() {
if (ph_entered == 0)
{   start();
    ph_entered = 1;
    pHmin = (float)atof(str_pHmin);
    pHmax = (float)atof(str_pHmax);
}

  float V_pot=analogRead(A1);
   //float t=((T-298)*0.000198+0.05916)*7;
  float V=(V_pot*3.292/1012.0);      //used for test board
  float pH=7.0+((F*(V_supply-V))/(R*T*C));
  //Serial.print("V,");
  //Serial.println(V);
       if (pH<pHmin) {
         digitalWrite(base, HIGH);
  digitalWrite(acid, LOW);
  Serial.print("pH,");
  Serial.println(pH);
          delay(200);
         }
         if (pH>pHmax) {
             digitalWrite(acid, HIGH);
             digitalWrite(base, LOW);
             Serial.print("pH,");
             Serial.println(pH);
             delay(200);
         }
         else {
                      digitalWrite(acid, LOW);
                      digitalWrite(base, LOW);
                      Serial.print("pH,");
                      Serial.println(pH);

                  }
}

