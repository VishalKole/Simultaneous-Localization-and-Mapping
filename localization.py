#!/usr/bin/env python

import rospy, cv2 as cv, matplotlib.image as mpimg, numpy as np, math
from mapGUI import Mapper
from nav_msgs.msg import OccupancyGrid
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from p2os_msgs.msg import SonarArray
import numpy as np

import Tkinter as tk
from PIL import Image
import ImageTk
import random
import rospy
from sensor_msgs.msg import LaserScan


WIDTH = 2000
HEIGHT = 700
PARTICLE_SIZE = 10

class Pose():
	def __init__(self,x,y,t):
		self.x = x
		self.y = y
		self.theta = t


class Particle():

	def __init__(self,x,y,t,w):
		self.pose = Pose(x,y,t)
		self.weights= w


class ParticleFilter():

	def init_with_values(self):
		
		area = np.arange(-0.8, 0.8, 0.1)
		locations =  [(8.0, -0.5, math.pi/2), (-12.0, 	12.0, math.pi), (-18.4, -8.9, 0), \
			   (10.8, 12.7, math.pi),(-54.5, 7.6, math.pi/2), (8.0, -1.5, math.pi/2)]
		theta = [ -0.2, -0.1 , 0, 0.1, 0.2 ]

		for i in locations:
			for x in area:
				for y in area:
					for t in theta:
						self.particles.append(Particle(i[0]+x,i[1]+y,i[2]+t,0.0))
					

	def __init__(self,m):
		
		self.mapper = m
		self.odom = None
		self.laser= None
		self.sonar = None
		self.particles = list()
		self.init_with_values()
		#self.init_particles()
		self.img = mpimg.imread('/home/fac/catkin_ws/src/hw3/src/project.png')


	def predict(self):
		"""
		compute delta(odom) and apply to each particle
		"""
		
		# current robot position
		xr    = self.odom.pose.pose.position.x
		yr    = self.odom.pose.pose.position.y
		z     = self.odom.pose.pose.orientation.z
		w     = self.odom.pose.pose.orientation.w
		thetar = 2*math.atan2(z,w)	
		dist = math.sqrt(xr**2 + yr**2)
		
		# translate and rotate the particles
		particles.pose.xp =  particles.pose.xp + xr
		particles.pose.yp =  particles.pose.yp + yr
		particles.pose.thetap = particles.pose.thetap + thetar
		
			
	def update(self):
		self.mapper.particle_update(self.particles)
		self.mapper.getReading(8.0, -0.5, math.pi/2)
	
	def resample(self):
		pass
	
	
	def odom_callback(self,data):
		self.odom= data
		self.update()
		

	def laser_callback(self,data):
		self.laser = data
		
	def sonar_callback(self,data):
		self.sonar = data

		
		
def main():
	
	root = tk.Tk()
	m = Mapper(master=root,height=WIDTH,width=HEIGHT)
	
	pf = ParticleFilter(m)
	rospy.init_node("particle_filter", anonymous=True)
	rospy.Subscriber("/r1/odom", Odometry, pf.odom_callback, queue_size = 1)
	rospy.Subscriber("/r1/kinect_laser/scan", LaserScan, pf.laser_callback, queue_size = 1)
	rospy.Subscriber("/r1/sonar", SonarArray, pf.sonar_callback, queue_size = 1)
	root.mainloop()

if __name__== "__main__":
	try:
		main()
	except rospy.ROSInterruptException:
		print("rospy.ROSInterruptException")