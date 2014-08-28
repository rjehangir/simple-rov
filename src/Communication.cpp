#include "Communication.h"

namespace {
	Transfer transfer;
}

namespace Communication {
	void init(Stream* _stream) {
		transfer.setStream(_stream);
	}

	void receive() {

	}

	void send() {
		
	}
}