"""Sample Webots controller for highway driving benchmark."""

from vehicle import Driver
import math

def min(a, b):
    if a < b:
        return a
    else:
        return b
        
def min3(a, b, c):
    if a < b and a < c:
        return a
    elif b < a and b < c:
        return b
    else:
        return c

# name of the available distance sensors
sensorsNames = [
    'front',
    'front right 0',
    'front right 1',
    'front right 2',
    'front left 0',
    'front left 1',
    'front left 2',
    'rear',
    'rear left',
    'rear right',
    'right',
    'left']
sensors = {}

maxSpeed = 100
driver = Driver()
driver.setSteeringAngle(0.0)  # go straight

# get and enable the distance sensors
for name in sensorsNames:
    sensors[name] = driver.getDistanceSensor('distance sensor ' + name)
    sensors[name].enable(10)

# get and enable the GPS
gps = driver.getGPS('gps')
gps.enable(10)

# get the camera
camera = driver.getCamera('camera')
# uncomment those lines to enable the camera
# camera.enable(50)
# camera.recognitionEnable(50)

while driver.step() != -1:
    # adjust the speed according to the value returned by the front distance sensor
    frontDistance = sensors['front'].getValue() 
    frontRange = sensors['front'].getMaxValue()
    SF = (frontRange - frontDistance) / frontRange
    
    RF0 = sensors['front right 0'].getValue()
    RF1 = sensors['front right 1'].getValue()
    RF2 = sensors['front right 2'].getValue()
    frontRightDistance = (RF0 + RF1 + RF2) / 3
    frontRightRange = 15
    SFR = (frontRightRange - min(frontRightDistance, frontRightRange)) / frontRightRange
    
    LF0 = sensors['front left 0'].getValue()
    LF1 = sensors['front left 1'].getValue()
    LF2 = sensors['front left 2'].getValue()
    frontleftDistance = (LF0 + LF1 + LF2) / 3
    frontLeftRange = 15
    SFL = (frontLeftRange - min(frontleftDistance, frontLeftRange)) / frontLeftRange
    
    rightDistance = sensors['right'].getValue()
    rightRange = 7
    SR = (rightRange - min(rightDistance, rightRange)) / rightRange
    
    leftDistance = sensors['left'].getValue()
    leftRange = 3
    SL = (2 - min(leftDistance, 2)) / 2
    SL2 = (leftDistance - 2) / 13
    
    MR = maxSpeed - 0.2 * SL - 0.1 * SL2 - 0.4 * SFL
    ML = maxSpeed - 0.1 * SL - 0.4 * SL2 - 0.0 * SFL
    # MR = maxSpeed - 0.5 * SF - 050 * SFR - 0.6 * L2L - 0.5 * SR - 0.8 * SL
    # ML = maxSpeed - 0.6 * SF - 0.6 * SFR - 0.3 * SFR - 0.6 * SR - 0.5 * SL
    
    driver.setSteeringAngle(10*math.pi/180 * (ML - MR))
    
    speed = maxSpeed * frontDistance / frontRange
    # speed = maxSpeed * min3(frontDistance / frontRange, frontRightDistance / frontRightRange, frontleftDistance / frontLeftRange)
    driver.setCruisingSpeed(speed)
    # brake if we need to reduce the speed
    speedDiff = driver.getCurrentSpeed() - speed
    if speedDiff > 0:
        driver.setBrakeIntensity(min(speedDiff / speed, 1))
    else:
        driver.setBrakeIntensity(0)
