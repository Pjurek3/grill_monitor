import requests
import datetime


def record_temp(manual_temp: int):
	"""records manual temp and recorded temp for calibration"""
	 
	# Append 'hello' at the end of file

	url = "http://192.168.0.104:8080/configure"
	a = requests.get(url)
	
	data = a.text.strip('\r\n')
	dt = datetime.datetime.utcnow()
	return {'dt': dt, 'actual': manual_temp, 'resistance': data}
	

