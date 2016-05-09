int analog_red=0;
int analog_ir=0;
int count=0;

int redPin=A0;
int irPin=A1;

void setup() {
    
    TCCR0A = 0x02;     // DISABLE PWM ON DIGITAL PINS 5 and 6, AND GO INTO CTC MODE
    TCCR0B = 0x05;     // DON'T FORCE COMPARE, 1024 PRESCALER 
    OCR0A = 0XFA;      // SET THE TOP OF THE COUNT TO 250 FOR 62.5Hz SAMPLE RATE or 16 ms
    TIMSK0 = 0x02;     // ENABLE INTERRUPT ON MATCH BETWEEN TIMER2 AND OCR2A
    sei();             // MAKE SURE GLOBAL INTERRUPTS ARE ENABLED
    Serial.begin(9600);  
    
}

ISR(TIMER0_COMPA_vect){        // triggered when Timer2 counts to 250(16 ms)
  count++;
  if(count==15)//send only after 240 ms.
  {
  count=0;
  cli();                                      // disable interrupts while we do this
  analog_red = analogRead(redPin);
  analog_ir = analogRead(irPin);
  //Serial.print("Working--ISR");
  Serial.print(analog_red);
  Serial.print(" ");
  Serial.println(analog_ir);
  sei();
  }
} 

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.print("Working");
}
