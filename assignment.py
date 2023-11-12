from __future__ import print_function
import os 


import time
from sr.robot import *




R = Robot()

# Threshold for the control of the linear distance
a_th = 2.0
# Threshold for the control of the orientation
d_th = 0.4
# Lists that store the golden tokens that have already been paired
lst_golden_tokens = []
my_time = 0.5 # turn and drive time


def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

#--------------------------------------------------------------------------

#This Function find the closest token nearby (among the tokens that were previously grabbed and put next to each other)
def find_near_token():
   
	distance = 100
	rotation_y = 0
	token_code = -1
	
	for token in R.see():
		if token.dist < distance and token.info.marker_type == MARKER_TOKEN_GOLD and token.info.code in lst_golden_tokens:
			distance = token.dist
			rotation_y = token.rot_y
			token_code = token.info.code
			
	if distance == 100:
	
		return -1 , -1 ,-1
	
	else:
		return distance, rotation_y ,token_code




while 1:
    
    Index = 1

while Index:       
  Distance, Rotation = find_token_gold()
  while Distance == -1:
      print("No tokens found!!")
      turn(5,0.5)
      Distance, Rotation = find_token_gold()
  
      
  if Distance < d_th:
      print("Found it!")
      R.grab()  # if we are close to the token, we grab it.
      print("Gotcha!")
      Index = 0
  elif -a_th <= Rotation <= a_th:  # if the robot is well aligned with the token, we go forward
      print("Ah, here we are!.")
      drive(10, 0.8)
  elif Rotation < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
      print("Left a bit...")
      turn(-2, 0.5)
  elif Rotation > a_th:
      print("Right a bit...")
      turn(+2, 0.5)
    
turn(-8,1.5)
drive(30,6)
R.release()

drive(-20,1.5)
turn(-10,4)
drive(20,2)  

Index2 = 0
while Index2 < 5 :

        Distance, Rotation = find_token_gold()
    
        while Distance == -1:
            print("I don't see any more tokens. Still searching")
            turn(+5, 0.5)
            Distance, Rotation = find_token_gold()
            
        if Distance < d_th:
            print("Found it!")
            R.grab()  # If we are close to the token, we grab it.
            print("Gotcha!")
            turn(20, 2.5)  # Adjust robot position for the next box placement
      	    # Move to the reference position
    	    drive(22, 6)   
            
            R.release()  # Release the box
            # Move away from the reference position
            drive(-20, 1.5)
            turn(-10, 4)
            drive(20, 2)
            Index2 = Index2 + 1
        elif -a_th <= Rotation <= a_th:  # If the robot is well aligned with the token, move forward
            print("Ah, here we are!.")
            drive(10, 0.8)
        elif Rotation < -a_th:  # If the robot is not well aligned with the token, move left
            print("Left a bit...")
            turn(-2, 0.5)
        elif Rotation > a_th:
            print("Right a bit...")
            turn(+2, 0.5)
      
