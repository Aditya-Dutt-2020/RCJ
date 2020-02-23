import serialPi
import buttonStopper as bs
import piCam
import greenDetectAditya as greenDetect # This may be brians or aditya's -- currently Adityas. Further testing needed.
#import ballDetection 


def main():
	serialPi.initSerial()
	bs.initButton()
	piCam.initialize()

	progStop = False
	inBallRoom = False

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

		if inBallRoom:
				move, amount = ballDetection.detectBall(frame)
				if amount:
					amount = ''.join(["0" for x in range(3-len(str(amount)))])+str(amount)

			if move != "skip":
				serialPi.write("stop")
				if move == "forw":
					serialPi.write("move"+amount+"f")
				elif move == "left":
					serialPi.write("turn"+amount+"l")
				elif move == "right":
					serialPi.write("turn"+amount+"r")
				serialPi.write("cont")
			elif move == "skip": # there are no balls in vision
				serialPi.write("stop")
				seriaPi.write("turn001l")  #can also go right, or go more 
				serialPi.write("cont")

			continue
		
		else:
			inBallRoom = silverDetection.detectSilver()


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


main()