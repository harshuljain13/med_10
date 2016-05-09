#include "I2Cdev.h"
#include "MPU6050.h"

// Arduino Wire library is required if I2Cdev I2CDEV_ARDUINO_WIRE implementation
// is used in I2Cdev.h
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

// class default I2C address is 0x68
// specific I2C addresses may be passed as a parameter here
// AD0 low = 0x68 (default for InvenSense evaluation board)
// AD0 high = 0x69
MPU6050 accelgyro;
//MPU6050 accelgyro(0x69); // <-- use for AD0 high

int count=0;
int flag=0;
float ax_arr[50];
float ay_arr[50];
float az_arr[50];

float sumx=0;
float sumy=0;
float sumz=0;

float ax_prev=0;
float ay_prev=0;
float az_prev=0;

int16_t ax, ay, az;
int16_t gx, gy, gz;


void setup() {
    // join I2C bus (I2Cdev library doesn't do this automatically)
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

    // initialize serial communication
    // (38400 chosen because it works as well at 8MHz as it does at 16MHz, but
    // it's really up to you depending on your project)
    Serial.begin(9600);

    // initialize device
    Serial.println("Initializing I2C devices...");
    accelgyro.initialize();

    // verify connection
    Serial.println("Testing device connections...");
    Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
}

void loop() {
    // read raw accel/gyro measurements from device
    accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    // these methods (and a few others) are also available
    //accelgyro.getAcceleration(&ax, &ay, &az);
    //accelgyro.getRotation(&gx, &gy, &gz);

        // display tab-separated accel/gyro x/y/z values
        float ax1=(float)ax/2048;
        float ay1=(float)ay/2048;
        float az1=(float)az/2048;    // these methods (and a few others) are also available
        float gyrox = (float)gx/131;
        float gyroy = (float)gy/131;
        float gyroz = (float)gz/131;			
        float angax = 57.295* atan(ax1 / sqrt(pow(ay1,2)+pow(az1,2)));
        float angay = 57.295* atan(ay1 / sqrt(pow(ax1,2)+pow(az1,2)));
        float angaz = 57.295* atan(az1 / sqrt(pow(ax1,2)+pow(ay1,2)));
        float compl_gyrox=((0.98)*(compl_gyrox + gyrox*0.01)+(0.02)*(angax))*180/3.14;
        float compl_gyroy=((0.98)*(compl_gyroy + gyroy*0.01)+(0.02)*(angay))*180/3.14;
        float compl_gyroz=((0.98)*(compl_gyroz + gyroz*0.01)+(0.02)*(angaz))*180/3.14;

//        Serial.print("a/g:\t");
//        Serial.print(ax1); Serial.print("\t");
//        Serial.print(ay1); Serial.print("\t");
//        Serial.print(az1); Serial.print("\t");
//        Serial.print(compl_gyrox); Serial.print("\t");
//        Serial.print(compl_gyroy); Serial.print("\t");
//        Serial.println(compl_gyroz);
        
        if(count==50){
         count=0; 
         flag=1;
        }
        
        sumx+=ax1;
        sumy+=ay1;
        sumz+=az1;
        
        if(flag==0){
        ax_arr[count]=ax1;
        ay_arr[count]=ay1;
        az_arr[count]=az1;
        }
        else{
        sumx-=ax_arr[count];
        ax_arr[count]=ax1;
        sumy-=ay_arr[count];
        ay_arr[count]=ay1;
        sumz-=az_arr[count];
        az_arr[count]=az1;
        }
        
        
         if(ax1>=(ax_prev+1.5) || ax1<=(ax_prev-1.5) || ay1>=(ay_prev+1.5) || ay1<=(ay_prev-1.5) || az1>=(az_prev+1.5) || az1<=(az_prev-1.5))
        Serial.println("motion");
        
        ax_prev=sumx/50;
        ay_prev=sumy/50;
        az_prev=sumz/50;
        count++;
        
        
      

}
