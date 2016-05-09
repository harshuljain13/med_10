int analogInPin = A0;
int sensorValue = 0;

void setup()
{
    pinMode(9, OUTPUT);  //Set Pin 9 to output
    analogWrite(9,127); //Write PWM2 value to output on Pin 9
    setPwmFrequency(9, 1024);
    TCCR2A = 0x02;     // DISABLE PWM ON DIGITAL PINS 3 AND 11, AND GO INTO CTC MODE
    TCCR2B = 0x06;     // DON'T FORCE COMPARE, 256 PRESCALER 
    OCR2A = 0X7C;      // SET THE TOP OF THE COUNT TO 124 FOR 500Hz SAMPLE RATE
    TIMSK2 = 0x02;     // ENABLE INTERRUPT ON MATCH BETWEEN TIMER2 AND OCR2A
    
    sei();             // MAKE SURE GLOBAL INTERRUPTS ARE ENABLED
    Serial.begin(115200);  
}

ISR(TIMER2_COMPA_vect){                         // triggered when Timer2 counts to 250
  cli();                                      // disable interrupts while we do this
  sensorValue = analogRead(analogInPin);
  Serial.println(sensorValue);
  sei();
}

void loop() {
  while(1);
}

void setPwmFrequency(int pin, int divisor) {
  byte mode;
  if(pin == 5 || pin == 6 || pin == 9 || pin == 10) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 64: mode = 0x03; break;
      case 256: mode = 0x04; break;
      case 1024: mode = 0x05; break;
      default: return;
    }
    if(pin == 5 || pin == 6) {
      TCCR0B = TCCR0B & 0b11111000 | mode;
    } else {
      TCCR1B = TCCR1B & 0b11111000 | mode;
    }
  } else if(pin == 3 || pin == 11) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 32: mode = 0x03; break;
      case 64: mode = 0x04; break;
      case 128: mode = 0x05; break;
      case 256: mode = 0x06; break;
      case 1024: mode = 0x7; break;
      default: return;
    }
    TCCR2B = TCCR2B & 0b11111000 | mode;
  }
}
