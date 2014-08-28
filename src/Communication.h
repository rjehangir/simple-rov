#ifndef COMMUNICATION_H90278
#define COMMUNICATION_H90278

#include <WProgram.h>
#include "Transfer.h"

namespace Communication {
	struct receiveStruct {
		int16_t pilotRoll;
		int16_t pilotPitch;
		int16_t pilotYaw;
		int16_t pilotForward;
		int16_t pilotStrafe;
		int16_t pilotUp;
	};

	struct sendStruct {
		int16_t thruster[6];
		int16_t millivoltage;
		int16_t millicurrent;
	};

	void init(Stream* _stream);

	void receive();

	void send();
}