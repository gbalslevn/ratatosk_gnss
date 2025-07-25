# Ratatosk antenna decider
Decides which antenna to use based on the rotation of the balloon. The rotation (also reffered to as heading or azimuth) is determined from a multi antenna input using the [Septentrio Mosaic-H evaluation kit](https://www.septentrio.com/en/products/gnss-receivers/gnss-receiver-modules/mosaic-h-evaluation-kit) 

### Choosing the right antenna
Out of 4 possible antennas the one pointing the most directly to the groundstation should be chosen. In the two cases below, respectevely antenna 4 and antenna 2 is chosen. 

![balloon_rotation](balloon_rotation.png)

The 4 patch antennas A1, A2, A3, A4 should initially be placed such that 1 points to north/(front), 2 to east/(right) and so on. On initital placement if heading is 0° and the groundstation is located 270° relative to the balloon, antenna 4 is chosen. 


If the balloon then rotates s.t. the heading is 140° we calculate 

$$
(groundstationDirection - balloonRotation) \mod 360 
$$

in this case 

$$ 
(270 - 140) \mod 360 =130 
$$

Based on the initial placement of antennas configured for the cardinal directions we can see the heading 130° is closer to 90° than 180° meaning we choose antenna 2. If two antennas has the exact same distance to being the correct one, the one currently not selected is chosen.  

It should be calibrated where our north is. Meaning if A1 is located at \theta_A1 we know A2=\theta_A1 + 90 mod 360, A3=\theta_A1 + 180 mod 360 and so on



The fomula for calculating rotation: https://www.omnicalculator.com/other/azimuth#azimuth-formula

## Install instructions
1. Create the virtual environment `python3 -m venv venv`
2. Activate the virtual environment `source venv/bin/activate`
3. Install the required packages `python3 -m pip install -r requirements.txt` (use `py` instead of `python3` on windows) 
4. Add user to allow reading serial: `sudo usermod -a -G dialout $USER`, then restart (For Linux but not neccesary for raspberry pi dist of linux. If on Windows or MacOS figure out how to access serial)
5. run with `python3 nmeaparser.py`

Remember to set correct serial port and hardcode correct location of groundstation. 

## Updating dependencies
Do `python3 -m pip freeze > requirements.txt`

## Tests
Run tests `python3 tests/antennaselector_test.py`
