#ifndef CONTROL_H90278
#define CONTROL_H90278

#include <WProgram.h>
#include "Data.h"

namespace Control {
	extern int16_t thruster[];

	void calculate();

	void execute();
}

#endif