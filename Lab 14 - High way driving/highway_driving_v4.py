"""Sample Webots controller for highway driving benchmark."""

from vehicle import Driver

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

maxSpeed = 90
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

FRange = 15
RRange = 15
LRange = 15
FRRange = 15
FLRange = 15
while driver.step() != -1:
    
    frontDistance = sensors['front'].getValue()
    frontRange = sensors['front'].getMaxValue()
    SF = frontDistance / frontRange
    SR = sensors['right'].getValue() / RRange
    SL = sensors['left'].getValue() / LRange
    SFR0 = sensors['front right 0'].getValue() / FRRange
    SFR1 = sensors['front right 1'].getValue() / FRRange
    SFR2 = sensors['front right 2'].getValue() / FRRange
    SFR = (SFR0 + SFR1 + SFR2) / 3
    SFL0 = sensors['front left 0'].getValue() / FLRange
    SFL1 = sensors['front left 1'].getValue() / FLRange
    SFL2 = sensors['front left 2'].getValue() / FLRange
    SFL = (SFL0 + SFL1 + SFL2) / 3
    
    MR = 0.6 * (1 - SFL)
    ML = 0.2 * SL + 0.6 * (1 - SFR)
    driver.setSteeringAngle(0.174533 * (MR - ML))
    
    # adjust the speed according to the value returned by the front distance sensor
    speed = maxSpeed * SF 
    driver.setCruisingSpeed(speed)
    # brake if we need to reduce the speed
    speedDiff = driver.getCurrentSpeed() - speed
    if speedDiff > 0:
        driver.setBrakeIntensity(min(speedDiff / speed, 1))
    else:
        driver.setBrakeIntensity(0)
