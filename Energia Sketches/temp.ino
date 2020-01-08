int heater = 7;
int tempPot = 0;
int tempR = 10000;
int Setpoint = 30;

void setup()
{
    pinMode(tempPot, INPUT);
    pinMode(heater, OUTPUT);
    Serial.begin(9600);
}

void loop()
{
    int tempPot = analogRead(A4) ;
    float tempResistance=(tempPot*tempR)/(1023-tempPot);
    float tempT=-0.0027*tempResistance+52;
    Serial.print("<temperature,");
    Serial.print(tempT);
    Serial.println(">");
    
    if(tempT < Setpoint+0.5)
        digitalWrite(heater, HIGH);
    
    else if(tempT > Setpoint+0.5)
        digitalWrite(heater, LOW);
    
    else if(Setpoint-0.5 < tempT < Setpoint+0.5)
        digitalWrite(heater, LOW);
    
    if (Serial.available() > 0 && Serial.read() == '<')
    {
        char input[25];
        int charsRead = Serial.readBytesUntil('>', input, 25);
        input[charsRead] = '\0';
        char* subsystem = strtok(input, ",");
        char* ptr2 = strtok(NULL, ",");
        Serial.print(ptr);
        Serial.print(" ");
        Serial.println(ptr2);
        double val = atof(ptr2);
        
        if (val != Setpoint)
            Setpoint = val;
    }
    delay(200);
}
