int heart_high, heart_low;
int data[200], i, mapped;
void setup(){
  for(i=2; i<12; i++)//LEDs
  pinMode(i, OUTPUT);
Serial.begin(115200);//for the processing sketch
  
}//setup


void loop(){

      heart_high=0;//reset the high before we look for it,  everything is higher than 0
      heart_low = 1023;//reset the low before we look for it, everything is lower than 1023
      
      for(i=200; i>0; i--){//search for the low and high out of the last 200 samples
        data[i] = data[i-1];// move everything back one, this will leave data[0] empty, but we put the next read there after this
        
      if(data[i]>heart_high)//check to see if we have something higher than the current high
      heart_high=data[i];//if it is higher, write the new value in
      if(data[i]<heart_low)//same idea as the high check
      heart_low=data[i];
    }//for loop
    
    data[0] = analogRead(0);//now write the next analog value to data[0]
    
    mapped = map(data[0], 0, 1023, 0, 600);
    Serial.println(mapped);//send over the current value to the processing sketch, but scale it to match the screen height

  delay(5);//delay in here is important, we need enough samples to catch an entire waveform, so at least 1 sec of samples should be tored in data[0], 
  //so 5ms x 200 = 1000, we're good
  
  
  //This code is where we control the LEDs
  if((heart_high-heart_low)>150){//first, don't even go in here unless the span of the high and low is greater than 150.  This is important, so the LEDs don't go crazy 
  //if you're flat lined
  
  //I'll explain how one of these works
  //There is an 'if' check for each of the LEDs
  //Basically, how this works is we want the LEDs turn represent the entire span of a heart beat, which is why we get the lowest and highest value
  //this gives us the span, which can be used to take a percentage of, and that's exactly how all these statements work
  if(data[0] > (heart_high-.95*(heart_high-heart_low)))//this is true if the read is greater than 95% of the span
  digitalWrite(2, HIGH);
  else
  digitalWrite(2,LOW); 
  
  if(data[0] > (heart_high-.9*(heart_high-heart_low)))// greater than 90% of the span and so on
  digitalWrite(3, HIGH);
  else
  digitalWrite(3,LOW); 
 
    if(data[0] > (heart_high-.8*(heart_high-heart_low)))
  digitalWrite(4, HIGH);
  else
  digitalWrite(4,LOW); 
    if(data[0] > (heart_high-.7*(heart_high-heart_low)))
  digitalWrite(5, HIGH);
  else
  digitalWrite(5,LOW); 
    if(data[0] > (heart_high-.6*(heart_high-heart_low)))
  digitalWrite(6, HIGH);
  else
  digitalWrite(6,LOW); 
    if(data[0] > (heart_high-.5*(heart_high-heart_low)))
  digitalWrite(7, HIGH);
  else
  digitalWrite(7,LOW); 
    if(data[0] > (heart_high-.4*(heart_high-heart_low)))
  digitalWrite(8, HIGH);
  else
  digitalWrite(8,LOW); 
    if(data[0] > (heart_high-.3*(heart_high-heart_low)))
  digitalWrite(9, HIGH);
  else
  digitalWrite(9,LOW); 
     if(data[0] > (heart_high-.2*(heart_high-heart_low)))
  digitalWrite(10, HIGH);
  else
  digitalWrite(10,LOW); 
     if(data[0] > (heart_high-.1*(heart_high-heart_low)))
  digitalWrite(11, HIGH);
  else
  digitalWrite(11,LOW);  
  
  }//span check
  else
  for(i=2; i<12; i++)//turn all the LEDs off if we're flatlined
  digitalWrite(i,LOW);
  


    

}//loop


