const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
unsigned char rawData[80];
const float sample_freq =34;

//unsigned int i=0;
int sensorValue = 0;        // value read from the pot
int len = sizeof(rawData);
int i,k;
long sum, sum_old;
int thresh = 0;
float freq_per = 0;
byte pd_state = 0;
  
void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  
}

void loop() {
   // read the analog in value:
  for(i=0;i<len;i++)
  {
  sensorValue = analogRead(analogInPin);
  rawData[i]=sensorValue;
  // print the results to the serial monitor:
  //Serial.print("\nsensor = " );
  //Serial.print(sensorValue);
  delay(30);
  }
  
  sum = 0;
  pd_state = 0;
  int period = 0;
  // Autocorrelation
  for(i=0; i < len; i++)
  {
    sum_old = sum;
    sum = 0;
    for(k=0; k < len-i; k++) sum += (rawData[k])*(rawData[k+i])/256;
    
    // Peak Detect State Machine
    if (pd_state == 2 && (sum-sum_old) <=0) 
    {
      period = i;
      pd_state = 3;
    }
    if (pd_state == 1 && (sum > thresh) && (sum-sum_old) > 0) pd_state = 2;
    if (!i) {
      thresh = sum * 0.5;
      pd_state = 1;
    }
  }
  // Frequency identified in Hz
  freq_per = sample_freq/period;
  Serial.print("\nfreq=");
  Serial.println(freq_per);
  
}
