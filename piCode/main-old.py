import serialPi
import buttonStopper as bs
import piCam
import greenDetect

def Main():
	serialPi.initSerial()
	bs.initButton()
	piCam.initialize()

	progStop = False

	while 1:
		if bs.getButton():
			progStop = not progStop
			if progStop == False:
				serialPi.write("cont")
			else:
				serialPi.write("stop")
		if progStop:
			continue

		frame = piCam.getFrame()
		move = greenDetect.detectGreen(frame)
		if move != "skip":
			serialPi.write("stop")
			if move == "U":
				serialPi.write("turn180l")
			elif move == "left":
				serialPi.write("turn090l")
			elif move == "right":
				serialPi.write("turn090r")
			serialPi.write("cont")

	# Some how end program.
	piCam.endprogram()


if "__name__" == __main__:
	Main()
