"""scripts to calculate steins heart equation

reference: https://www.newport.com/medias/sys_master/images/images/h67/hc1/8797049487390/AN04-Thermistor-Calibration-and-Steinhart-Hart.pdf"""

def c_from_f(f):
    celcius = ((f - 32) * 5/9)
	return celcius

def calibrate(inputs):
    """calibrates stein-hearts equation based off 
	method 1.  The input is a dict with the T/R inputs.  The output is a dict with the constants
	
	input: 
		{1: 
			{'r': 123,
			 't': 70},
			 {'r': 500,
			 't': 30},
			 {'r': 900,
			 't': 120},
			 }
			 """
	