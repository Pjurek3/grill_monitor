"""this script runs the microcontroller as a web server.  This allows
outside items to ping the server and get data"""

try:
    import usocket as socket
except:
    import socket

response_404 = """HTTP/1.0 404 NOT FOUND

<h1>404 Not Found</h1>
"""

response_500 = """HTTP/1.0 500 INTERNAL SERVER ERROR

<h1>500 Internal Server Error</h1>
"""

response_template = """HTTP/1.0 200 OK

%s
"""

import machine
import ntptime, utime
from machine import RTC, Pin
from time import sleep

rtc = RTC()
food = Pin(5, Pin.OUT)
grill = Pin(4, Pin.OUT)
led = Pin(9, Pin.OUT)
switch_pin = Pin(10, Pin.IN)
temp_pin = machine.ADC(0)
print(temp_pin.read())

try:
    seconds = ntptime.time()
except:
    seconds = 0
rtc.datetime(utime.localtime(seconds))

def time():
    body = """<html>
<body>
<h1>Time</h1>
<p>%s</p>
</body>
</html>
""" % str(rtc.datetime())

    return response_template % body

def get_food_temp():
    """returns foote temp"""
    grill.value(0)
    food.value(1)
    return temp_pin.read()


def get_grill_temp():
    """returns grill temp"""
    food.value(0)
    grill.value(1)
    return temp_pin.read()

def temperature(measurements=20):
    """
    captures temperature readings and reports out results
    
    parameters
    -------
    measurements: int
        positive integer which controls how many measurements are made in 
        reading.
    
    results
    --------
    
    """
    # get food temp
    food_temps = []
    grill_temps = []
    for i in range(measurements):
        food_temps.append(get_food_temp())
        # get grill temp
    for i in range(measurements):
        grill_temps.append(get_grill_temp())
    
    food_temp = sum(food_temps)/len(food_temps)
    grill_temp = sum(grill_temps)/len(grill_temps)
    # return results
    body = "{food_temp: " + str(food_temp) + ", grill_temp: " + str(grill_temp) +  "}"
    return response_template % body

def temperature(measurements=20):
    """
    captures temperature readings and reports out results
    
    parameters
    -------
    measurements: int
        positive integer which controls how many measurements are made in 
        reading.
    
    results
    --------
    
    """
    # get food temp
    food_temps = []
    grill_temps = []
    for i in range(measurements):
        food_temps.append(get_food_temp())
        # get grill temp
        grill_temps.append(get_grill_temp())
    
    food_temp = sum(food_temps)/len(food_temps)
    grill_temp = sum(grill_temps)/len(grill_temps)
    # return results
    body = "{food_temp: " + str(food_temp) + ", grill_temp: " + str(grill_temp) +  "}"
    return response_template % body


handlers = {
    'temperature': temperature,
    'temperature_v02': temperature_v02
}

def main():
    s = socket.socket()
    ai = socket.getaddrinfo("0.0.0.0", 8080)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080")
    print(addr)

    while True:
        sleep(1)
        res = s.accept()
        client_s = res[0]
        client_addr = res[1]
        req = client_s.recv(4096)
        print("Request:")
        print(req)

        try:
            path = req.decode().split("\r\n")[0].split(" ")[1]
            handler = handlers[path.strip('/').split('/')[0]]
            print(handler)
            response = handler()
        except KeyError:
            response = response_404
        except Exception as e:
            response = response_500
            print(str(e))

        client_s.send(b"\r\n".join([line.encode() for line in response.split("\n")]))

        client_s.close()
        print()

main()