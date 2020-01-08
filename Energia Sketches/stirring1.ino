int readCurrent = 35;//read Iout from photo-interrupter sq wave
int controlMotor = 32 ; //output PWM to motot
int Vcc1 = 40; // interupter
int Vcc2 = 39; // LED on interrupter
int GND1 = 18;
int GND2 = 17;

int motorSpeed = 255;
int recordTime =0;
int recordRotation=0;
int lastCurrent = 0;
int newCurrent=0;

int realRange = 600;
int lowerRange = realRange -20;
int upperRange = realRange +20;

void setup() {
  // put your setup code here, to run once:
pinMode(readCurrent,INPUT);
pinMode(controlMotor,OUTPUT);
pinMode(Vcc1,OUTPUT);
pinMode(Vcc2,OUTPUT);
pinMode(GND1,OUTPUT);
pinMode(GND2,OUTPUT);

Serial.begin(9600);

}

void loop() {
    // lights up LED2- photointerrupter
    digitalWrite(Vcc2,HIGH);
    digitalWrite(Vcc1,HIGH);
    digitalWrite(GND2,LOW);
    digitalWrite(GND1,LOW);

    //get the speed of rotation, read per 20ms, caculate per 20s,1000round
    newCurrent = digitalRead(readCurrent);
    //Serial.println(newCurrent);
    //Serial.println(newCurrent);
    if (newCurrent != lastCurrent){
        if (newCurrent == 1){
            recordRotation = recordRotation+1;
        }
    }
    lastCurrent = newCurrent;
    //Serial.println(recordTime);
    if (recordTime % 2000 == 0 ){
        int RPM = recordRotation *30/2;
        recordRotation=0;
        // control the speed  per 20s
        if (RPM == 0){ //first time
            //Serial.println(motorSpeed);
            analogWrite(controlMotor,motorSpeed);
        }
        else if (RPM >= upperRange && motorSpeed>0){ // too fast
            motorSpeed = motorSpeed -1;

        }

        else if (RPM <= lowerRange && motorSpeed<255){
            motorSpeed  = motorSpeed+1;
        }
        Serial.println("\n\nRPM: ");
        Serial.println(RPM);
        analogWrite(controlMotor,motorSpeed);
        Serial.println("The motor Speed: ");
        Serial.println(motorSpeed);

    }
    recordTime =recordTime+5;

    delay(5);//perform every 20ms

  // put your main code here, to run repeatedly: 

}
