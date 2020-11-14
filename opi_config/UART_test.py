from time import sleep
import serial
import OPi.GPIO as GPIO


class UartMessageHandler(object):
    def __init__(self):
        self.bufferSize = 5  # Frame of 5  bytes
        self.ser = serial.Serial(port="/dev/ttyS1", baudrate=9600, timeout=0.1)
        self.connect_flag = False
        self.header = 0x7E  # First byte in frame

    def connect(self):
        GPIO.setboard(GPIO.ZEROPLUS2H5)
        GPIO.setmode(GPIO.SOC)          # set up SOC numbering

        reset_gpio = GPIO.PA + 2        # Pin for Arduino reset
        GPIO.setup(reset_gpio, GPIO.OUT)
        GPIO.output(reset_gpio, 0)

        while not self.connect_flag:
            # Restart arduino
            GPIO.output(reset_gpio, 1)
            sleep(0.7)
            GPIO.output(reset_gpio, 0)
            sleep(3)
            # Connect to Arduino
            self.handle_in_msg()

    def handle_in_msg(self):
        buff_raw = self.ser.read_until(size=self.bufferSize)
        buff_proc, err = self.check_msg(buff_raw)
        print buff_proc, err
        if not err:
            self.perform_routine(buff_proc)

    def perform_routine(self, buff_proc):
        if buff_proc[1] == 0x50:
            print "Connection with arduino is done"
            self.send_to_uart(0x51, 0x00, 0x00)  # Prove to arduino that connection is done
            self.connect_flag = True

        elif buff_proc[1] == 0x35:
            print "Movement is detected"

    def check_msg(self, buff):
        buff = [ord(byte) for byte in buff]
        if len(buff) > 0:
            if buff[0] == self.header and sum(buff[:-1]) == buff[4]:

                return buff, False

        return buff, True

    def send_to_uart(self, code, par1, par2):  # Create outgoing message
        buffer_out = [self.header, code, par1, par2]
        buffer_out += [sum(buffer_out)]

        for byte in buffer_out:
            self.ser.write(chr(byte))   # Write 5 bytes (frame) to serial

        print "Outgoing message: ", buffer_out

    def close(self):
        GPIO.cleanup()
        self.ser.close()


msg_handler = UartMessageHandler()

try:
    msg_handler.connect()

    while True:
        msg_handler.handle_in_msg()
        sleep(0.5)
        # msg_handler.send_to_uart(0x21, 0x00, 0x00)
        # sleep(5)
        msg_handler.send_to_uart(0x33, 0x00, 0x00)


except KeyboardInterrupt:
    msg_handler.close()



# while ser.isOpen():
#     if ser.inWaiting() > 0:
#         accept_message_from_uart()
#         # send to socket
#     else:
#         # receive (timeout=0.1)
#         code1 = input("Type code: ")
#         print code1
#         param2 = 0
#         if (code1 == 0x24) or (code1 == 0x30):
#             param2 = input("Type param2: ")
#             print param2
#         send_to_uart(code1, 0x00, param2)

#
# elif buff_proc[1] == 0x38:
#     res = "Highlighted"

# else:
#     print "Unknown command"