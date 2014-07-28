#include <WProgram.h>
#include "MPU6000.h"
#include "HMC5883.h"
#include "DCM.h"
#include "APM.h"

float dt;
long timer;
long outputTimer;
long diagnosticTimer;

void setup() {
  Serial.begin(57600);
  Serial.println("start");

  // Set barometer CS pin high so it doesn't hog the bus. How frustrating.  
  pinMode(40,OUTPUT);
  digitalWrite(40,HIGH);
  
  APM::init();
  MPU6000::init();
  HMC5883::init();
  DCM::init();
  
  if (false) {
	  HMC5883::calibrateOffsets();
	}
	HMC5883::set_offset(108, 6, 96);
}

void updateNavigationSensors() {
	// Update IMU + compass
	if ( MPU6000::newdata ) {
    
    dt = (micros()-timer)/1000000.0f;
    timer = micros();
    
    MPU6000::read();
    HMC5883::read();
    HMC5883::calculate(DCM::roll,DCM::pitch);
    HMC5883::applyDeclination(12.4);
    DCM::updateMeasurements(MPU6000::gyroY,
			      MPU6000::gyroX,
			      -MPU6000::gyroZ,
			      -MPU6000::accelY,
			      -MPU6000::accelX,
			      MPU6000::accelZ,
			      dt);
    DCM::normalize();
    DCM::driftCorrection(HMC5883::heading);
    DCM::accelerationCorrection();
    DCM::convertDCMtoEuler();
    
    if (false) {
			Serial.println(HMC5883::heading);
	  }
  
	  if (false) {
			Serial.print(degrees(DCM::roll));Serial.print(" ");
			Serial.print(degrees(DCM::pitch));Serial.print(" ");
			Serial.print(degrees(DCM::yaw));Serial.print(" ");
			Serial.print(degrees(HMC5883::heading));Serial.println(" ");
	  }
  
	  if (false) {
			Serial.print(-MPU6000::accelY);Serial.print(" ");
			Serial.print(-MPU6000::accelX);Serial.print(" ");
			Serial.print(-MPU6000::accelZ);Serial.print(" ");
			Serial.print(MPU6000::gyroY);Serial.print(" ");
			Serial.print(MPU6000::gyroX);Serial.print(" ");
			Serial.print(-MPU6000::gyroZ);Serial.println(" ");
	  }
  }
}

void loop() {
	static const long printPeriod			=			500;
  static const long controlPeriod   =     20; // 50 Hz

	static long printTimer;
	static long controlTimer;

	if (millis()-controlTimer>controlPeriod) {
		controlTimer = millis();

  	updateNavigationSensors();

  }	
  
  if (false && millis()-printTimer > printPeriod) {
  	printTimer = millis();
		Serial.write(27);       // ESC command
		Serial.print("[2J");    // clear screen command
		Serial.write(27);
		Serial.print("[H");     // cursor to home command
		Serial.println("BlueROV Live Data");
		Serial.println("=====================");
		Serial.print("Roll: ");Serial.print(degrees(DCM::roll));Serial.println(" deg ");
		Serial.print("Pitch: ");Serial.print(degrees(DCM::pitch));Serial.println(" deg");				
  	Serial.println("");  	
  }
}
