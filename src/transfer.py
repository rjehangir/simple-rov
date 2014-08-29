import Queue
import struct
import crcmod

def decodeTransfer(queue,formatString):
	length = struct.calcsize(formatString)

	if ( queue.empty() ):
		return

	preamble = ['\xFF','\xFA'];
	input = [0x00,0x00]
	input[1] = queue.get(0,0)
	print input[1]
	while ( True ):
		if ( input == preamble ):
			break
		else:
			if ( queue.empty() ):
				return
			input[0] = input[1]
			input[1] = queue.get(0,0)

	if queue.qsize() < length + 2:
		return

	#Get data
	data = ''
	for i in range(length):
		data += queue.get()

	#Get checksum
	input = queue.get()
	input += queue.get()
	checksum = struct.unpack('H',input)[0]

	#Verify checksum
	crc16 = crcmod.mkCrcFun(0x11021,0xFFFF,True)
	calcChecksum = crc16(data)
	calcChecksum = (~calcChecksum) % 2**16  # convert to uint16_t

	if ( checksum != calcChecksum ):
		print "Failed checksum."
		return
	      
	return struct.unpack(formatString,data)

def encodeTransfer(formatString,values):
	header = '\xFF\xFA'
	data = struct.pack(formatString,*values)
	crc16 = crcmod.mkCrcFun(0x11021,0xFFFF,True)
	calcChecksum = crc16(data)
	calcChecksum = (~calcChecksum) % 2**16  # convert to uint16_t
	
	return header + data + struct.pack('H',calcChecksum)