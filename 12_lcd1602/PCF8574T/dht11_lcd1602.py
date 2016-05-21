#!/usr/bin/python

import RPi.GPIO as GPIO
import time

from i2clibraries import i2c_lcd

def scrollTextRightOnce(txt):
	str_pad = " " * 17
	my_long_string = txt
	my_long_string = str_pad + my_long_string

#	while True:
	for i in range (0, len(my_long_string)):
		lcd_text = my_long_string[i:(i+17)]
		lcd.setPosition(1, 0) 
		lcd.writeString(lcd_text)
		time.sleep(0.1)
		lcd.writeString(str_pad)
        
	
def scrollTextRight(txt):
	str_pad = " " * 17
	my_long_string = txt
	my_long_string = str_pad + my_long_string

	while True:
		for i in range (0, len(my_long_string)):
			lcd_text = my_long_string[i:(i+17)]
			lcd.setPosition(1, 0) 
			lcd.writeString(lcd_text)
			time.sleep(0.1)
			lcd.writeString(str_pad)

channel = 12
data = []
j = 0

# Configuration parameters
# I2C Address, Port, Enable pin, RW pin, RS pin, Data 4 pin, Data 5 pin, Data 6 pin, Data 7 pin, Backlight pin (optional)
lcd = i2c_lcd.i2c_lcd(0x27, 1, 2, 1, 0, 4, 5, 6, 7, 3)
lcd.backLightOn()
lcd.command(lcd.CMD_Display_Control | lcd.OPT_Enable_Display)


# If you want to disable the cursor, uncomment the following line
# lcd.command(lcd.CMD_Display_Control | lcd.OPT_Enable_Display)
#lcd.writeString("TEST")
#time.sleep(1)

GPIO.setmode(GPIO.BOARD)
time.sleep(1)



try:
	while True:
		data = []
		j = 0
		humidity = 0
		humidity_point = 0
		temperature = 0
		temperature_point = 0
		check = 0
		
		GPIO.setup(channel, GPIO.OUT)
		GPIO.output(channel, GPIO.LOW)
		time.sleep(0.05)
		GPIO.output(channel, GPIO.HIGH)

		GPIO.setup(channel, GPIO.IN)

		while GPIO.input(channel) == GPIO.LOW:
			continue

		while GPIO.input(channel) == GPIO.HIGH:
			continue

		while j < 40:
			k = 0
			while GPIO.input(channel) == GPIO.LOW:
				continue

			while GPIO.input(channel) == GPIO.HIGH:
				k += 1
				if k > 100:
					break

			if k < 8:
				data.append(0)
			else:
				data.append(1)

			j += 1

		print ("sensor is working.")
		print (data)

		humidity_bit = data[0:8]
		humidity_point_bit = data[8:16]
		temperature_bit = data[16:24]
		temperature_point_bit = data[24:32]
		check_bit = data[32:40]

		humidity = 0
		humidity_point = 0
		temperature = 0
		temperature_point = 0
		check = 0

		for i in range(8):
			humidity += humidity_bit[i] * 2 ** (7 - i)
			humidity_point += humidity_point_bit[i] * 2 ** (7 - i)
			temperature += temperature_bit[i] * 2 ** (7 - i)
			temperature_point += temperature_point_bit[i] * 2 ** (7 - i)
			check += check_bit[i] * 2 ** (7 - i)

		tmp = humidity + humidity_point + temperature + temperature_point

		if check == tmp:
			print ("Temperature: ", temperature, ", Humidity: " , humidity)
			#lcd.writeString("TEST")
#			scrollTextRightOnce("Temperature: " + str(temperature)+ ", Humidity: " + str(humidity))
			lcd.setPosition(1, 0) 
			lcd.writeString("Temperature: " + str(temperature))
			lcd.setPosition(2, 0) 
			lcd.writeString("Humidity: " + str(humidity))
		else:
			print ("wrong")
			print ("temperature : ", temperature, ", humidity : " , humidity, " check : ", check, " tmp : ", tmp)
		time.sleep(5)
except KeyboardInterrupt:
	GPIO.cleanup()
	
	


	
#time.sleep(5)
GPIO.cleanup()
