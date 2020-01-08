int RUNNING = 1;
int DELAY = 100;

int pHpin=A1; //pH vars
int acid_LED=39;
int base_LED=40;
float F=9.6485309e4;
float phR=8.314510;
int phT=290;
float V_supply=0.66;
float C=2.302585;
float pH;
float a;
float b;
float pHmin = 6.5;
float pHmax = 7.5;

int heater = 7; //temperature vars
int Pot = 0;
int tempR = 10000;
int Setpoint = 30; 
float tempT;

//stirring vars
int readCurrent = 35;//read Iout from photo-interrupter sq wave
int controlMotor = 32 ; //output PWM to motot
int Vcc1 = 40; // interupter
int Vcc2 = 39; // LED on interrupter
int GND1 = 18;
int GND2 = 17;

int motorSpeed = 255;
int recordTime = 0;
int recordRotation=0;
int lastCurrent = 0;
int newCurrent=0;
int RPM;

int realRange = 600;
int lowerRange = realRange -20;
int upperRange = realRange +20;

void setup() {
    pinMode(acid_LED, OUTPUT); //pH setup
    pinMode(base_LED, OUTPUT);
    pinMode(pHpin, INPUT);

    pinMode(Pot, INPUT); //temperature setup
    pinMode(heater, OUTPUT);

    pinMode(readCurrent,INPUT); //stirring setup
    pinMode(controlMotor,OUTPUT);
    pinMode(Vcc1,OUTPUT);
    pinMode(Vcc2,OUTPUT);
    pinMode(GND1,OUTPUT);
    pinMode(GND2,OUTPUT);

    Serial.begin(9600);
}

int update_variables() {
    if ((char)Serial.read() == '<')
    {
        char input[25];
        int charsRead = Serial.readBytesUntil('>', input, 25);
        input[charsRead] = '\0';
        if (strcmp("stop", input) == 0) {
            RUNNING = 0;
            return 0;
        }
        char* subsystem = strtok(input, ",");
        char* ptr2 = strtok(NULL, ",");
        double value = atof(ptr2);
        if (strcmp("pH", subsystem) == 0) {
            pH = value;
        }
        else if (strcmp("temperature", subsystem) == 0) {
            Setpoint = value;
        }
        else if (strcmp("speed", subsystem) == 0) {
            motorSpeed = value;
        }
    }
    return 1;
}

void read_pH()
{
    float V_pot = analogRead(A1);
    float t=((T-298)*0.000198+0.05916)*7;
    float V = V_pot*3.3/1012.0;      //used for test board

    //read pH value from UI if available here
    float pH = 7.0+((F*(V_supply-V))/(phR*phT*C));
         if (pH < pHmin) {
               digitalWrite(base_LED, HIGH);
               digitalWrite(acid_LED, LOW);
           }
           if (pH > pHmax) {
               digitalWrite(base_LED, LOW);
               digitalWrite(acid_LED, HIGH);
           }
           else {
               digitalWrite(acid_LED, LOW);
               digitalWrite(base_LED, LOW);
           }
}

void read_temperature()
{
    int Pot = analogRead(A4);
    float resistance=(Pot*tempR)/(1023-Pot);
    tempT=-0.0027*resistance + 52;

    if(tempT < Setpoint+0.5)
        digitalWrite(heater, HIGH);

    else if(tempT > Setpoint+0.5)
        digitalWrite(heater, LOW);

    else if(Setpoint-0.5 < tempT  && tempT < Setpoint+0.5)
        digitalWrite(heater, LOW);
}

void read_speed()
{
    // lights up LED2- photointerrupter
    digitalWrite(Vcc2,HIGH);
    digitalWrite(Vcc1,HIGH);
    digitalWrite(GND2,LOW);
    digitalWrite(GND1,LOW);

    //get the speed of rotation, read per 20ms, caculate per 20s,1000round
    newCurrent = digitalRead(readCurrent);
    if (newCurrent != lastCurrent){
        if (newCurrent == 1){
            recordRotation = recordRotation+1;
        }
    }
    lastCurrent = newCurrent;
    if (recordTime % 2000 == 0 ){
        int RPM = recordRotation *30/2;
        recordRotation=0;
        if (RPM == 0){ //first time
            analogWrite(controlMotor,motorSpeed);
        }
        else if (RPM >= upperRange && motorSpeed>0){ // too fast
            motorSpeed = motorSpeed -1;
        }
        else if (RPM <= lowerRange && motorSpeed<255){
            motorSpeed  = motorSpeed+1;
        }
    }
    recordTime = recordTime+5;
}

void loop() {
    if (RUNNING == 1) {
        if (Serial.available() > 0) {
            RUNNING = update_variables();
        }
        else {
            read_pH();
            read_temperature();
            read_speed();
        }

        Serial.print("<pH,");
        Serial.print(pH);
        Serial.println(">");
        delay(DELAY);
        Serial.print("<temperature,");
        Serial.print(tempT);
        Serial.println(">");
        delay(DELAY);
        Serial.print("<speed,");
        Serial.print(RPM);
        Serial.println(">");
        delay(DELAY);
    }
    else {
        exit(0);
    }
}

