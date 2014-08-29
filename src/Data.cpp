#include "Data.h"
#include "Control.h"
#include "APM.h"

namespace Data {
	receiveStruct in;
	sendStruct    out;

	void update() {
		for ( uint8_t i = 0 ; i < 6 ; i++ ) {
			out.thruster[i] = Control::thruster[i];
		}
		out.millivoltage = APM::getVoltage()*1000;
		out.millicurrent = APM::getCurrent()*1000;
	}
}