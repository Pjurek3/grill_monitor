import gc
import webrepl
#webrepl.start()
gc.collect()

import network
import time
import machine
import secrets
print('configuring')

sta_if = network.WLAN(network.STA_IF); sta_if.active(True)


for connection in connections:
    station, password = connection

    print("Connecting to {}.".format(station))

    sta_if.connect(station, password)

    for i in range(15):
        print(".")

        if sta_if.isconnected():
            break

        time.sleep(1)

    if sta_if.isconnected():
        break
    else:
        print("Connection could not be made.\n")

print('done configuring')