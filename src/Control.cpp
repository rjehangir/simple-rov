#include "Control.h"
#include "APM.h"

namespace {
	float controlRoll, controlPitch, controlYaw;
	float controlForward, controlStrafe, controlVertical;
}

namespace Control {
	int16_t thruster[6];
	
	void calculate() {
		controlRoll     = Data::in.pilotRoll;
		controlPitch    = Data::in.pilotPitch;
		controlYaw      = Data::in.pilotYaw;
		controlForward  = Data::in.pilotForward;
		controlStrafe   = Data::in.pilotStrafe;
		controlVertical = Data::in.pilotVertical;
	}

	void execute() {
		static const int16_t base = 1500;
		thruster[0] = base + controlRoll + 0.5*controlStrafe + 0.5*controlPitch + 0.5*controlVertical; // Front left vertical
		thruster[1] = base - controlRoll - 0.5*controlStrafe + 0.5*controlPitch + 0.5*controlVertical; // Front right vertical
		thruster[2] = base + controlYaw + controlForward; // Left forward
		thruster[3] = base - controlYaw + controlForward; // Right forward
		thruster[4] = base - controlPitch + controlVertical; // Back vertical
		thruster[5] = base + controlStrafe; // Bottom lateral

		for ( uint8_t i = 0 ; i < 6 ; i++ ) {
			APM::outputPWM(i,constrain(thruster[i],1100,1900));
		}
	}
}