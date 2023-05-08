from connectServer import*
from uart import *

time.sleep(HOLD_TIME_GLOBAL)
while True:
    # Confirm UART connection
    confirmUART(client)

    #Read data from sensor
    startMeasure(client)

    pass