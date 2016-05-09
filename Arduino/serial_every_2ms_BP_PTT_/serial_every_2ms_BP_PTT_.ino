#define F_CPU 16000000UL
#define USART_BAUDRATE 230400
#define UBRR_VALUE (((F_CPU / (USART_BAUDRATE * 16UL))))

int analog_red=0;
int analog_ir=0;
int redPin=A0;
int irPin=A1;

void USART0Init(void)
{
// Set baud rate
UBRR0H = 0x00;//(uint8_t)(UBRR_VALUE>>8);
UBRR0L = 0x08;//(uint8_t)UBRR_VALUE;
// Set frame format to 8 data bits, no parity, 1 stop bit
UCSR0A |= (1<<U2X0);
UCSR0C |= (1<<UCSZ01)|(1<<UCSZ00);
//enable transmission and reception
UCSR0B |= (1<<RXEN0)|(1<<TXEN0);
}

void USART0SendByte(uint8_t u8Data)
{
//wait while previous byte is completed
while(!(UCSR0A&(1<<UDRE0))){};
// Transmit data
UDR0 = u8Data;
}

void setup() {
   // Initializes Timer2 to throw an interrupt every 2mS.
  TCCR2A = 0x02;     // DISABLE PWM ON DIGITAL PINS 3 AND 11, AND GO INTO CTC MODE
  TCCR2B = 0x06;     // DON'T FORCE COMPARE, 256 PRESCALER 
  OCR2A = 0X7C;      // SET THE TOP OF THE COUNT TO 124 FOR 500Hz SAMPLE RATE
  TIMSK2 = 0x02;     // ENABLE INTERRUPT ON MATCH BETWEEN TIMER2 AND OCR2A
  USART0Init();
  sei();             // MAKE SURE GLOBAL INTERRUPTS ARE ENABLED      
}

ISR(TIMER2_COMPA_vect){        // triggered when Timer2 counts to 2ms
  cli();                                     // disable interrupts while we do this
  analog_red = analogRead(redPin);
  analog_ir = analogRead(irPin);
  //Serial.print("Working--ISR");
  //Serial.println(analogRead(redPin));//analog_red);
  //Serial.println("-");
  //Serial.println(500);
  //Serial.print("\n");
  //delayMicroseconds(1);
  
  USART0SendByte((analog_red/100)+48);
  USART0SendByte(((analog_red%100)/10)+48);
  USART0SendByte(((analog_red%100)%10)+48);
  USART0SendByte(' ');
  
  USART0SendByte((analog_ir/100)+48);
  USART0SendByte(((analog_ir%100)/10)+48);
  USART0SendByte(((analog_ir%100)%10)+48);
  USART0SendByte('\n');
  sei();
} 

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.print("Working");
}
