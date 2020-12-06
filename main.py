import network
import machine
from utime import sleep, sleep_ms
import ntptime, utime
import urequests
import secrets
import ujson

__version__ = 'V0.2.0'

# defines the interval between taking readings in seconds
READINGS_INTERVAL_SECONDS = 60 # seconds

led = machine.Pin(2, machine.Pin.OUT)

def deep_sleep(msecs):
  #configure RTC.ALARM0 to be able to wake the device
  rtc = machine.RTC()
  rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
  # set RTC.ALARM0 to fire after Xmilliseconds, waking the device
  rtc.alarm(rtc.ALARM0, msecs)
  #put the device to sleep
  machine.deepsleep()


def blink():
    """blinks led briefly"""
    led.value(0)
    sleep(1)
    led.value(1)

def send_data(reading):
    """sends the dict data to the adafruit IO

    assume reading is provided with dict with food_temp, grill_temp keys and 
    integer readings as values"""
    # post data
    URL = 0
    data_field = 1
    base_url = 'https://io.adafruit.com'

    mapper = [('/api/v2/{}/feeds/food-temp/data', 'food_temp'),
            ('/api/v2/{}/feeds/grill-temp/data', 'grill_temp'),]
    for item in mapper:
        url = base_url + item[URL].format(secrets.ADAFRUIT_IO_USERNAME)
        headers = {'x-aio-key': secrets.ADAFRUIT_IO_KEY,
                'Content-Type': 'application/json',
                }
        data = {'value': reading[item[data_field]]}
        print(data)
        response = urequests.post(url=url, headers=headers, data=ujson.dumps(data))
        print(response.__dict__)

rtc = machine.RTC()
food = machine.Pin(5, machine.Pin.OUT)
grill = machine.Pin(4, machine.Pin.OUT)
switch_pin = machine.Pin(10, machine.Pin.IN)
temp_pin = machine.ADC(0)
print(temp_pin.read())

try:
    seconds = ntptime.time()
except:
    seconds = 0
rtc.datetime(utime.localtime(seconds))


def food_value():
    """returns foote temp"""
    grill.value(0)
    food.value(1)
    return temp_pin.read()


def grill_value():
    """returns grill temp"""
    food.value(0)
    grill.value(1)
    return temp_pin.read()

def v_2_f(v):
    """
    converts the voltage reading to fareingheit based off calibration of probe
    
    parameters
    -------
    v: numeric reading of the voltage read from the probe
    
    results
    --------
    conversion to fareignheit based off calibration
    
    """
    return 0.2552 * v + 68.905

def get_temperature(measurements=20):
    """
    function to calculate the temperature and voltage reading
    
    parameters
    -------
    measurements: int representing the number of readings to smooth over
    
    results
    --------
    dict of temperatures and voltages read
    
    """
    # get food temp
    food_readings = []
    grill_readings = []
    print('getting food reading')
    for i in range(measurements):
        food_readings.append(food_value())
        # get grill temp
        sleep_ms(100)
    
    print('getting grill reading')
    for i in range(measurements):
        grill_readings.append(grill_value())
        sleep_ms(100)
    print(grill_readings)

    food_v = sum(food_readings)/len(food_readings)
    grill_v = sum(grill_readings)/len(grill_readings)
    print('converting to f')
    food_t = v_2_f(food_v)
    grill_t = v_2_f(grill_v)
    print('step3')
    return {'food_voltage': food_v,
            'food_temp': food_t, 
            'grill_voltage': grill_v,
            'grill_temp': grill_t}

def main():

    blink()
    print('getting readings')
    readings = get_temperature(2)
    blink()
    print(readings)
    print('sending data')
    send_data(readings)
    blink()
    print('going to sleep for ', READINGS_INTERVAL_SECONDS, ' seconds')
    sleep(READINGS_INTERVAL_SECONDS)


print('starting up')
main()
deep_sleep(READINGS_INTERVAL_SECONDS * 1000)
