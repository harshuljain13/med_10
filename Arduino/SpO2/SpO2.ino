int PWM1 = 50;     // PWM1 width
int PWM2 = 50;     // PWM2 width
int analog_red=0;
int analog_ir=0;
int count=0;

int red_min=1023,ir_min=1023,red_max=0,ir_max=0;
float red_ac,ir_ac;
float R,SpO2;

int redPin=A0;
int irPin=A1;

void setup() {
    TCNT1=0x7FFF;        //Set Timer1 Counter Register to half of its maximum value (32767)
    pinMode(9, OUTPUT);  //Set Pin 9 to output
    pinMode(11, OUTPUT); //Set Pin 11 to output
    analogWrite(9, PWM1); //write PWM1 value to output on Pin 9
    analogWrite(11,PWM2); //Write PWM2 value to output on Pin 11
    
    TCCR0A = 0x02;     // DISABLE PWM ON DIGITAL PINS 5 and 6, AND GO INTO CTC MODE
    TCCR0B = 0x05;     // DON'T FORCE COMPARE, 1024 PRESCALER 
    OCR0A = 0XFA;      // SET THE TOP OF THE COUNT TO 250 FOR 62.5Hz SAMPLE RATE or 16 ms
    TIMSK0 = 0x02;     // ENABLE INTERRUPT ON MATCH BETWEEN TIMER2 AND OCR2A
    sei();             // MAKE SURE GLOBAL INTERRUPTS ARE ENABLED
    Serial.begin(115200);  
    
}

ISR(TIMER0_COMPA_vect){        // triggered when Timer0 counts to 250(16 ms)
  count++;
  if(count==5)//send only after 96 ms.
  {
  count=0;
  cli();                                      // disable interrupts while we do this
  analog_red = analogRead(redPin);
  analog_ir = analogRead(irPin);
  
  if(analog_red>red_max)
  red_max=analog_red;
  
  else if(analog_red<red_min)
  red_min=analog_red;
  
  if(analog_ir>ir_max)
  ir_max=analog_ir;
  
  else if(analog_ir<ir_min)
  ir_min=analog_ir;
  
  red_ac= (red_max-red_min);
  ir_ac= (ir_max-ir_min);
  
  R= (red_ac/red_min)/(ir_ac/ir_min);
  SpO2= 110 - 20*R;
  
  Serial.print("\nSpO2:");
  Serial.print(SpO2);
  Serial.print("\nR:");
  Serial.print(R);
//  Serial.print("\nir_ac:");
//  Serial.print(ir_ac);
//  Serial.print("\nred_ac");
//  Serial.print(red_ac);
//  
//  Serial.print("\nir_max:");
//  Serial.print(ir_max);
//  
//  Serial.print("\nir_min:");
//  Serial.print(ir_min);
//  
//  Serial.print("\nred_max:");
//  Serial.print(red_max);
//  
//  Serial.print("\nred_min:");
//  Serial.print(red_min);
//  Serial.print("R");
//  Serial.print(analog_red);
//  Serial.print("I");
//  Serial.print(analog_ir);
//  Serial.print("\n");
  sei();
  }
  
} 


void loop() {
  
  
}
/*
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
*/
