int analogInPin = A0;
int sensorValue = 0;
int count=0;
void setup() { 
  // Initializes Timer2 to throw an interrupt every 2mS.
  TCCR2A = 0x02;     // DISABLE PWM ON DIGITAL PINS 3 AND 11, AND GO INTO CTC MODE
  TCCR2B = 0x07;     // DON'T FORCE COMPARE, 1024 PRESCALER 
  OCR2A = 0XFA;      // SET THE TOP OF THE COUNT TO 250 FOR 62.5Hz SAMPLE RATE
  TIMSK2 = 0x02;     // ENABLE INTERRUPT ON MATCH BETWEEN TIMER2 AND OCR2A
  sei();             // MAKE SURE GLOBAL INTERRUPTS ARE ENABLED
  Serial.begin(9600);  
}

ISR(TIMER2_COMPA_vect){        // triggered when Timer2 counts to 250(16 ms)
  count++;
  if(count==5)//send only after 80 ms.
  {
  count=0;
  cli();                                      // disable interrupts while we do this
  sensorValue = analogRead(analogInPin);
  Serial.println(sensorValue);
  sei();
  }
} 

void loop() {
  // put your main code here, to run repeatedly:
  while(1);

}
