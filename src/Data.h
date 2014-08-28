#ifndef DATA_H90278
#define DATA_H90278

#include <WProgram.h>

namespace Data {
	struct receiveStruct {
		int16_t pilotRoll;
		int16_t pilotPitch;
		int16_t pilotYaw;
		int16_t pilotForward;
		int16_t pilotStrafe;
		int16_t pilotVertical;
	};

	struct sendStruct {
		int16_t thruster[6];
		int16_t millivoltage;
		int16_t millicurrent;
	};

	extern receiveStruct in;
	extern sendStruct    out;

	void update();
}

#endif