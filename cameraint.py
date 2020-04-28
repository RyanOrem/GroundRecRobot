from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
from subprocess import call

###############################################################
#                                                             #
#                 Ground Reconaissance Robot                  #
#                                                             #
###############################################################
#                           Team 20                           #
# Ryan Orem                                                   #
# Cody Randig                                                 #
# Pulakit Mishra                                              #
# Yousef Abu Khalifa                                          #
###############################################################
#                     TABLE OF CONTENTS                       #
# Section 1: Creating File Name for Video                     #
#     1A: Read in Number List from File Into an Array         #
#     1B: Append Next Value to the Number List File           #
#     1C: Add New Value into Array, Create File Name String   #
# Section 2: Flickering Blue Light to Indicate Pi is ON       #
#     2A: Setting Up GPIO for Flickering                      #
#     2B: Flickering the Light                                #
# Section 3: Turn Camera and Light On                         #
#     3A: Setting Up GPIO for Button                          #
#     3B: Button Logic                                        #
#     3C: Turn Camera On                                      #
#     3D: Turn Light On                                       #
# Section 4: Turn Camera and Light Off                        #
#     4A: Button Logic                                        #
#     4B: Turn Camera and Light Off                           #
#     4C: Turn Raspberry Pi Off                               #
###############################################################



#Section 1:  Creating File Name for Video
#Section 1A: Read in Number List from File Into an Array
vid_val = []                                                    #creates array to read what number for video file
with open('/media/usb/vidlist.txt') as f:                       #Opens txt file as variable f
    for line in f:                                              #creates a for loop that iterates through file
        vid_val.append(line)                                    #adds value from file into array
f.close()                                                       #closes file


#Section 1B:  Append Next Value to the Number List File
if len(vid_val)==0:                                             #checks to see if file is empty             
    vid_v = open('/media/usb/vidlist.txt', "a")                 #allows us to append the file saved as variable vid_v
    vid_v.write("0")                                            #Adds 0 to file
    vid_v.write("\n")                                           #adds an enter to file
    vid_v.close()                                               #closes file
else:
    new_val = int(vid_val[len(vid_val) - 1].strip()) + 1        #deletes the enter or \n from string, converts string to int to get value as a numeric(1/2)
                                                                #value and then adds one to it to get next number (2/2)
    vid_v = open('/media/usb/vidlist.txt', "a")                 #allows us to append the file saved as vid_v
    vid_v.write(str(new_val))                                   #adds new valaue to file
    vid_v.write("\n")                                           #adds a /n to file:enter
    vid_v.close()                                               #closes file
    
     
#Section 1C:  Add New Value into Array, Create File Name String   
with open('/media/usb/vidlist.txt') as f:                                    #opens text file as f
    for line in f:                                                           #for loop used to iterater through file
        vid_val.append(line)                                                 #add values from txt file into array 
f.close()                                                                    #closes file
vid_name = "/media/usb/vid" + vid_val[len(vid_val) - 1].strip() + ".h264"    #vidoe name starts with file location, vollowed by vid followed by new(1/2)
                                                                             #value, then file type (2/2)



#Section 2:  Flickering Blue Light to Indicate Pi is ON
#Section 2A:  Setting Up GPIO for Flickering
GPIO.setmode(GPIO.BCM)                 #Set mode of GPIO 
GPIO.setwarnings(False)                #ignore warnings of bad GPIO
GPIO.setup(23, GPIO.OUT)               #Allow access to GPIO23


#Section 2B: Flickering the Light
i=0                                    #declares an iterator = 1
while(i<10):                           #will allow only 10 full cycles of flickering
    GPIO.output(23,GPIO.LOW)           #Turns on light
    sleep(.25)                         #pauses code for 0.25 seconds
    GPIO.output(23,GPIO.HIGH)          #Turns off the light
    sleep(.25)                         #pauses code for 0.25 seconds
    i = i + 1                          #one cycle complete, moves iterator up one


#Section 3: Turn Camera and Light On
#Section 3A: Setting Up GPIO for Button
GPIO.setmode(GPIO.BCM)                                   #Sets up GPIO pin
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)      #declares GPIO 18 for the button


#Section 3B: Button Logic 
while True:                                              #will continuously run
    input_state = GPIO.input(18)                         #sets a variable equal to the binary value of the button
    if input_state == False:                             #if not pressed, enter if statement
        sleep(0.2)                                       #wait 0.2 seconds before checking next value of button
    else:                                                #if button pushed, enter this else statement
        break                                            #Break out of while loop



#Section 3C: Turn Camera On
camera = PiCamera()                                      #opens camera connected to raspberry pi
camera.resolution=(1280,720)                             #sets resolution of camera
camera.framerate = 68                                    #sets FPS of camera
camera.start_recording(vid_name)                         #begins recording and saves to variable vid_name


#Section 3D: Turn Light On
GPIO.output(23,GPIO.LOW)                                 #turns light on to indicate camera is recording
sleep(5)                                                 #set to 5 second pause so user doesnt press button once, but value was read in twice while (1/2)
                                                         #user's finger on button

#Section 4: Turn Camera and Light Off 
#Section 4A:  Button Logic
while True:                                              #continuously runs while loop until button is pressed
    input_state = GPIO.input(18)                         #value pf button saves to a variable
    if input_state == False:                             #if button is not press, enter branch
        sleep(0.2)                                       #wait 0.2 seconds and check button value again
    else:                                                #button is pressed 
        break                                            #breaks while lloop when button is pressed


#Section 4B: Turn Camera and Light Off
GPIO.output(23,GPIO.HIGH)                               #turns light off
camera.stop_recording()                                 #stops recording on camera


#Section 4C: Turn Raspberry Pi Off 
sleep(5)                                                #pause code for five seconds to allow time to save video
#call("sudo shutdown -h now", shell=True)               #turns off pi.  So user does not corrupt pi by unplugging it