'''
 * USBDisplayGame.py
 *
 * Copyright (c) 2020 seeed technology co., ltd.
 * Author      : weihong.cai (weihong.cai@seeed.cc)
 * Create Time : Aug 2020
 * Change Log  :
 *
 * The MIT License (MIT)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
 * documentation files (the "Software"), to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
 * and to permit persons to whom the Software istm furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions
 * of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
 * THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS INcommInterface
 * THE SOFTWARE.
 *
 * Get started:
 *     1. Download the pyusb library use pip3:
 *         $ pip3 install pyusb
 *     2. Go to the python-demo path:
 *         $ cd ~/seeed-linux-usbdisp/drivers/python-demo/
 *     3. Run demo:
 *         $ sudo python3 USBDisplayGame.py
'''

import usb.core
import usb.util
import struct
import time
import random

from PIL import Image

import RPi.GPIO as GPIO

#------Please choose one of them according to the WioTerminal Demo--------#
# NullFunctional_Demo_for_WioTerminal
# displayEndpointAddr = 0x04

# USBDisplayAndMouseControl_Demo_for_WioTerminal
displayEndpointAddr = 0x05
#-------------------------------------------------------------------------#

# find our device
devices = list(usb.core.find(find_all=True, idVendor=0x2886, idProduct=0x802D))

# for dev in devices:
# 	print(dev.serial_number)

# print(type(devices))
dev1 = devices[0]
dev2 = devices[1]
dev3 = devices[2]

# print("\n")
print("dev1:", dev1.serial_number)
print("dev2:", dev2.serial_number)
print("dev3:", dev3.serial_number)

# # was it found?
# if dev is None:
#     raise ValueError('Device not found')
if dev1 is None:
    raise ValueError('Device not found')
if dev2 is None:
    raise ValueError('Device not found')
if dev3 is None:
    raise ValueError('Device not found')

########################## fill screen ###################################################
'''
brief: Fill the whole screen with color

color: A 16 bit color represent in B5G6R5 format
dev1_on/dev2_on/dev3_on: Select which device to work
'''
def fillScreen(color, dev1_on, dev2_on, dev3_on):
	# fillScreen_color = random.randint(0, 65535)
	# fillScreen_color = 0xF800 # red
	# fillScreen_color = 0xFFFF # white
	# fillScreen_printOneTime = 0
	fillScreen_color = color
	fillScreen_header = 0x81
	fillScreen_index = "<BH"
	fillScreen_index_end = "<B"
	fillScreen_data = [fillScreen_header, fillScreen_color]

	fillScreen_package = struct.pack(fillScreen_index, *fillScreen_data)
	fillScreen_package_end = struct.pack(fillScreen_index_end, fillScreen_header)

	if(dev1_on):
		fillScreen_cnt = dev1.write(displayEndpointAddr, fillScreen_package)
		dev1.write(displayEndpointAddr, fillScreen_package_end)
	time.sleep(1)
	if(dev2_on):
		fillScreen_cnt = dev2.write(displayEndpointAddr, fillScreen_package)
		dev2.write(displayEndpointAddr, fillScreen_package_end)
	time.sleep(1)
	if(dev3_on):
		fillScreen_cnt = dev3.write(displayEndpointAddr, fillScreen_package)
		dev3.write(displayEndpointAddr, fillScreen_package_end)

	# if(fillScreen_printOneTime==0)
	# 	fillScreen_printOneTime=1
	print("fillScreen. Send %d byte(s) data." %fillScreen_cnt) # 3 bytes
	print("Write------->successful!\n")

	time.sleep(1)
##########################################################################################

############################### rect #####################################################
'''
brief    : Fill a rectangle of the display with a solid color

left     : The left boundry of the rectangle
top      : The top boundry of the rectangle
right    : The right boundry of the rectangle
bottom   : The bottom boundry of the rectangle
color    : A 16 bit color represent in B5G6R5 format
operation: The pixel bit operation will be done when filling the rectangle
dev1_on/dev2_on/dev3_on: Select which device to work
'''
def rect(left, top, right, bottom, color, operation, dev1_on, dev2_on, dev3_on):
	rect_header = 0x83
	rect_left = left
	rect_top = top
	rect_right = right
	rect_bottom = bottom
	# rect_printOneTime = 0
	# rect_color = random.randint(0, 65535)
	rect_color = color
	rect_operation = operation
	rect_index = "<BHHHHHB"
	rect_index_end = "<B"
	rect_data = [rect_header, rect_left, rect_top, rect_right, rect_bottom, rect_color, rect_operation]

	rect_package = struct.pack(rect_index, *rect_data)
	rect_package_end = struct.pack(rect_index_end, rect_header)

	if(dev1_on):
		rect_cnt = dev1.write(displayEndpointAddr, rect_package)
		dev1.write(displayEndpointAddr, rect_package_end)
	if(dev2_on):
		rect_cnt = dev2.write(displayEndpointAddr, rect_package)
		dev2.write(displayEndpointAddr, rect_package_end)
	if(dev3_on):
		rect_cnt = dev3.write(displayEndpointAddr, rect_package)
		dev3.write(displayEndpointAddr, rect_package_end)

	# rect_left = rect_left + 10
	# rect_right = rect_right + 10
	# if(rect_left==350):
	# 	rect_left = 0
	# 	rect_right = 100

	# time.sleep(0.5)

	# if(rect_printOneTime==0):
	# 	rect_printOneTime = 1
	print("rect. Send %d byte(s) data." %rect_cnt) # 12 bytes
	print("Write------->successful!\n")
##########################################################################################

############################# copyArea ###################################################
'''
brief : Copy a part of the existing image of the screen to another position of the display

sx    : Source x coordinate
sy    : Source y coordinate
dx    : Destination x coordinate
dy    : Destination y coordinate
width : Width of the copying area
height: Height of the copying area
dev1_on/dev2_on/dev3_on: Select which device to work
'''
def copyArea(sx, sy, dx, dy, width, height, dev1_on, dev2_on, dev3_on):
	# copyArea_printOneTime = 0
	copyArea_header = 0x84
	copyArea_sx = sx
	copyArea_sy = sy
	copyArea_dx = dx
	copyArea_dy = dy
	copyArea_width = width
	copyArea_height = height
	copyArea_index = "<BHHHHHH"
	copyArea_index_end = "<B"
	copyArea_data = [copyArea_header, copyArea_sx, copyArea_sy, copyArea_dx, copyArea_dy, copyArea_width, copyArea_height]

	copyArea_package = struct.pack(copyArea_index, *copyArea_data)
	copyArea_package_end = struct.pack(copyArea_index_end, copyArea_header)

	if(dev1_on):
		copyArea_cnt = dev1.write(displayEndpointAddr, copyArea_package)
		dev1.write(displayEndpointAddr, copyArea_package_end)
	if(dev2_on):
		copyArea_cnt = dev2.write(displayEndpointAddr, copyArea_package)
		dev2.write(displayEndpointAddr, copyArea_package_end)
	if(dev3_on):
		copyArea_cnt = dev3.write(displayEndpointAddr, copyArea_package)
		dev3.write(displayEndpointAddr, copyArea_package_end)

	# time.sleep(0.3)

	# if(copyArea_printOneTime==0):
	# 	copyArea_printOneTime = 1
	print("copyArea. Send %d byte(s) data." %copyArea_cnt) # 13 bytes
	print("Write------->successful!\n")
##########################################################################################

############################ bitblt ######################################################
'''
brief     : Draw image to the display

x         : The x coordinate where the image will be painted
y         : The y coordinate where the image will be painted
image_path: The path of image
operation : The pixel bit operation will be done between the original pixel and the pixel from the image
dev1_on/dev2_on/dev3_on: Select which device to work
'''
def bitblt(x, y, image_path,  operation, dev1_on, dev2_on, dev3_on):
	# image_path = "./image/img_20_30.png"
	# image = Image.open(image_path)
	image = Image.open(image_path)
	image = image.convert("RGB")
	image_data = []
	bitblt_width = image.width
	bitblt_height = image.height
	# bitblt_printOneTime = 0

	# print(type(image))
	# print(image)
	# print(image_data)

	# convert (R, G, B) -----> RGB565 (0xRGB)
	for y_ in range(bitblt_height):
		for x_ in range(bitblt_width):
			pixel = image.getpixel((x_, y_))
			# pixel = (pixel[0] + pixel[1] + pixel[2]) / 3
			R = ((pixel[0] >> 3) << 11) & 0xF800
			G = ((pixel[1] >> 2) << 5)  & 0x07E0
			B = ( pixel[2] >> 3)        & 0x001F
			RGB565_data = R | G | B
			image_data.append(RGB565_data)

	bitblt_start_header = 0x82
	bitblt_subpackage_header = 0x02
	bitblt_x = x
	bitblt_y = y

	image_size = bitblt_width * bitblt_height
	integer_part = (int)(image_size / 31)
	remainder_part = ((image_size) - (integer_part * 31))

	# while(True):
	bitblt_width = image.width
	bitblt_height = image.height
	bitblt_operation = operation
	bitblt_index_for_parameter = "<BHHHHB"
	bitblt_index_for_image = "<BHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"  # 1+31x2 = 63 bytes

	# bitblt_index_for_image_end = "<BHHHHHHHHHHH"  # 1+11x2 = 23 bytes
	bitblt_index_for_image_end = "<B"
	for i in range(remainder_part):
		bitblt_index_for_image_end = bitblt_index_for_image_end + 'H'

	# if(bitblt_printOneTime==0):
	print(bitblt_index_for_image_end)

	bitblt_index_end = "<B"

	bitblt_parameterData = [bitblt_start_header, bitblt_x, bitblt_y, bitblt_width, bitblt_height, bitblt_operation]
	# bitblt_subImageData = [bitblt_subpackage_header, subImageData]
	bitblt_subImageData_end = [bitblt_subpackage_header, *image_data[integer_part*31 : image_size]]

	bitblt_parameterPackage    = struct.pack(bitblt_index_for_parameter, *bitblt_parameterData)
	# bitblt_subImageDataPackage = struct.pack(bitblt_index_for_image, *bitblt_subImageData)
	bitblt_subImageDataPackage_end = struct.pack(bitblt_index_for_image_end, *bitblt_subImageData_end)
	bitblt_package_end         = struct.pack(bitblt_index_end, bitblt_start_header)

	if(dev1_on):
		dev1.write(displayEndpointAddr, bitblt_parameterPackage)
	if(dev2_on):
		dev2.write(displayEndpointAddr, bitblt_parameterPackage)
	if(dev3_on):
		dev3.write(displayEndpointAddr, bitblt_parameterPackage)

	# if(bitblt_printOneTime==0):
	print((int)(image_size / 31))
	print("integer_part:",integer_part)
	print("remainder_part:",remainder_part)

	for i in range(integer_part):
		bitblt_subImageData = [bitblt_subpackage_header, *image_data[i*31 : 31+i*31]]
		bitblt_subImageDataPackage = struct.pack(bitblt_index_for_image, *bitblt_subImageData)
		
		if(dev1_on):
			bitblt_cnt = dev1.write(displayEndpointAddr, bitblt_subImageDataPackage)
		if(dev2_on):
			bitblt_cnt = dev2.write(displayEndpointAddr, bitblt_subImageDataPackage)
		if(dev3_on):
			bitblt_cnt = dev3.write(displayEndpointAddr, bitblt_subImageDataPackage)

	if(dev1_on):
		dev1.write(displayEndpointAddr, bitblt_subImageDataPackage_end)
		dev1.write(displayEndpointAddr, bitblt_package_end)
	if(dev2_on):
		dev2.write(displayEndpointAddr, bitblt_subImageDataPackage_end)
		dev2.write(displayEndpointAddr, bitblt_package_end)
	if(dev3_on):
		dev3.write(displayEndpointAddr, bitblt_subImageDataPackage_end)
		dev3.write(displayEndpointAddr, bitblt_package_end)

	# time.sleep(0.4)

	# bitblt_x = bitblt_x + 20
	# if(bitblt_x == 320):
	# 	bitblt_x = 0
	# 	bitblt_y = bitblt_y + 30
	# 	if(bitblt_y > 210):
	# 		bitblt_y = 0

	# if(bitblt_printOneTime==0):
		# bitblt_printOneTime = 1
	print("bitblt. Send %d byte(s) data." %bitblt_cnt) # 63 bytes
	print("Write------->successful!\n")
##########################################################################################

############################ class #######################################################
class Bullet():
	def __init__(self, bullet_img, x, y):
		self.image = bullet_img
		self.speed = 20
		self.width = 10
		self.height = 10
		self.x = x
		self.y = y-(int)(self.height/2)
		self.is_hit = False

		bitblt(x=self.x, y=self.y, image_path=self.image, operation=0, \
			dev1_on=True, dev2_on=False, dev3_on=False)

	def move(self):
		# self.x = self.x + self.speed
		# bitblt(x=self.x, y=self.y, image_path=self.image, operation=0, \
		# 	dev1_on=True, dev2_on=False, dev3_on=False)
		# # rect(left=self.x-self.speed, top=self.y, right=self.x-self.speed+self.width, bottom=self.y+self.height, color=0xffff, operation=0, \
		# # 	dev1_on=True, dev2_on=False, dev3_on=False)
		# time.sleep(0.002)

		self.x = self.x + self.speed
		bitblt(x=self.x, y=self.y, image_path=self.image, operation=0, \
			dev1_on=True, dev2_on=False, dev3_on=False)
		if(self.speed >= self.width):
			rect(left=self.x-self.speed, top=self.y, right=self.x-self.speed+self.width, bottom=self.y+self.height, color=0xffff, operation=0, \
				dev1_on=True, dev2_on=False, dev3_on=False)
		else:
			rect(left=self.x-self.speed, top=self.y, right=self.x, bottom=self.y+self.height, color=0xffff, operation=0, \
				dev1_on=True, dev2_on=False, dev3_on=False)

class Player():
	def __init__(self, plane_img, x, y):
		self.image = plane_img
		self.x = x
		self.y = y
		self.width = 50
		self.height = 70
		self.speed_x = 50
		self.speed_y = 80
		self.is_hit = False
		
		bitblt(x=self.x, y=self.y, image_path=self.image, operation=0, \
			dev1_on=True, dev2_on=False, dev3_on=False)

	# def shoot(self, bullet_img):
	# 	bullet = Bullet(bullet_img, self.rect.midtop)
	# 	self.bullets.add(bullet)

	def shoot(self, bullet_img):
		# b = Bullet(bullet_img, self.x+self.width, self.y+self.height/2)
		return Bullet(bullet_img, self.x+self.width, (int)(self.y+self.height/2))
		# b.move()
		# bitblt(x=self.x, y=self.y, image_path=bullet_img, operation=0, \
		# 	dev1_on=True, dev2_on=True, dev3_on=True)

	def moveUp(self):
		self.x = 0

	def moveDown(self):
		self.x = 0

	def moveLeft(self):
		if(self.y == 5):
			self.y = 5
		else:
			self.y = self.y - self.speed_y
			if(self.y<=0):
				self.y = self.y + self.speed_y
			else:
				bitblt(x=self.x, y=self.y, image_path=self.image, operation=0, \
					dev1_on=True, dev2_on=False, dev3_on=False)
				rect(left=self.x, top=self.y+self.speed_y, right=self.x+self.width, bottom=self.y+self.speed_y+self.height, color=0xffff, operation=0, \
					dev1_on=True, dev2_on=False, dev3_on=False)
				time.sleep(0.002)

	def moveRight(self):
		if(self.y == 165):
			self.y = 168
		else:
			self.y = self.y + self.speed_y
			if(self.y>=240):
				self.y = self.y - self.speed_y
			else:
				bitblt(x=self.x, y=self.y, image_path=self.image, operation=0, \
					dev1_on=True, dev2_on=False, dev3_on=False)
				rect(left=self.x, top=self.y-self.speed_y, right=self.x+self.width, bottom=self.y-self.speed_y+self.height, color=0xffff, operation=0, \
					dev1_on=True, dev2_on=False, dev3_on=False)
				time.sleep(0.002)

class Enemy():
	def __init__(self, enemy_img, x, y):
		self.image = enemy_img
		self.x = x
		self.y = y
		self.width = 40
		self.height = 50
		self.speed = 8
		self.is_hit = False

		bitblt(x=self.x, y=self.y, image_path=self.image, operation=0, \
			dev1_on=True, dev2_on=False, dev3_on=False)

	def move(self):
		self.x = self.x - self.speed
		if(self.x<=0):
			self.x = 0
		bitblt(x=self.x, y=self.y, image_path=self.image, operation=2, \
			dev1_on=True, dev2_on=False, dev3_on=False)
		if(self.speed >= self.width):
			rect(left=self.x+self.speed, top=self.y, right=self.x+self.speed+self.width, bottom=self.y+self.height, color=0xffff, operation=0, \
				dev1_on=True, dev2_on=False, dev3_on=False)
		else:
			rect(left=self.x+self.width, top=self.y, right=self.x+self.speed+self.width, bottom=self.y+self.height, color=0xffff, operation=0, \
				dev1_on=True, dev2_on=False, dev3_on=False)
		time.sleep(0.002)
##########################################################################################

########################### main() #######################################################
def main():
	fillScreen(color=0xffff, dev1_on=True, dev2_on=True, dev3_on=True)
	plane_path = "./image/img_50_70.jpg"
	bullet_path = "./image/img_10_10.png"
	enemy_path = "./image/img_40_50.jpg"
	gameOver_path = "./image/img_100_240.jpg"

	buttonLeft_pin  = 22
	buttonRight_pin = 24
	buttonShoot_pin = 12
	
	# GPIO.setmode(GPIO.BOARD)
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(buttonLeft_pin,  GPIO.IN)
	GPIO.setup(buttonRight_pin, GPIO.IN)
	GPIO.setup(buttonShoot_pin, GPIO.IN)

	player = Player(plane_path, 0, 85)
	bullets = []
	bullets_temp = []
	enemies = []
	enemies_temp = []
	# enemy = Enemy(enemy_path, 280, random.choice([15,95,175]))

	previousTime = time.time()
	while(True):
		currentTime = time.time()
		timeDifference = (int)(currentTime - previousTime)

		buttonLeft_state  = GPIO.input(buttonLeft_pin)
		buttonRight_state = GPIO.input(buttonRight_pin)
		buttonShoot_state = GPIO.input(buttonShoot_pin)

		if(buttonLeft_state==GPIO.HIGH):
			player.moveLeft()
		if(buttonRight_state==GPIO.HIGH):
			player.moveRight()
		if(buttonShoot_state==GPIO.HIGH):
			bullets.append(player.shoot(bullet_path))

		if(timeDifference != 0):
			if(timeDifference % 5 == 0):
				previousTime = time.time()
				enemies.append(Enemy(enemy_path, 280, random.choice([15,95,175])))

		for e in enemies:
			enemy_y = e.y + e.height/2
			player_y = player.y + player.height/2

			if(enemy_y==player_y):
				if(e.x<=player.width):
					player.is_hit = True
					break
			elif(e.x<=0):
				# bitblt(x=110, y=0, image_path=gameOver_path,  operation=0, \
				# 		dev1_on=True, dev2_on=True, dev3_on=True)
				player.is_hit = True
				break

			for b in bullets:
				bullet_y = b.y + b.height/2
				if(enemy_y==bullet_y):
					if(b.x>=320):
						b.is_hit = True
					if(b.x>=e.x):
						e.is_hit = True
						b.is_hit = True
				else:
					if(b.x>=320):
						b.is_hit = True

		bullets_temp = bullets
		index1 = 0
		for b in bullets:
			if not b.is_hit:
				b.move()
			else:
				bullets_temp.pop(index1)
				if(index1==0):
					index1 = 0
				else:
					index1 = index1 - 1
			index1 = index1 + 1
		bullets = bullets_temp

		enemies_temp = enemies
		index2 = 0
		for e in enemies:
			if not e.is_hit:
				e.move()
			else:
				rect(left=e.x, top=e.y, right=e.x+e.width, bottom=e.y+e.height, color=0xffff, operation=0, \
					dev1_on=True, dev2_on=False, dev3_on=False)
				enemies_temp.pop(index2)
				if(index2==0):
					index2 = 0
				else:
					index2 = index2 - 1
			index2 = index2 + 1
		enemies = enemies_temp

		# time.sleep(1)

		if(player.is_hit == True):
			bitblt(x=110, y=0, image_path=gameOver_path,  operation=0, \
						dev1_on=True, dev2_on=True, dev3_on=True)
			break

if __name__ == '__main__':
	main()
