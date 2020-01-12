import serial
turndeg = 5
s1 = serial.Serial('COM6', 115200)
s1.flushInput()

comp_list = [b"Flash Complete\r\n", b"Hello Pi, this is arduino UNO...\r\n"]
while True:
    # inputValue = s1.readline()
    # print(inputValue)
    n = input("Input a stop or go Code: ")
    s1.write(str.encode(n))
    print("done")
