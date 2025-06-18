# Notes
We will be using either the moasic or AsteRX for GNSS https://www.septentrio.com/en/products/gnss-receivers
These has a multiantenna setup where we can also determine azimuth. Out of 4 possible antennas the one pointing the most directly should be chosen based on the azimuth of the balloon. 

We should calculate azimuth based on two points. We get azimuth by calcultating a line (also reffered to as the baseline vector) between two GNSS antennas, providing us with the direction of the balloon. Then use that direction to compare with the direction of the ground station. Based on that, turn on a specific antenna. 

The fomula for calculating rotation: https://www.omnicalculator.com/other/azimuth#azimuth-formula

GNSS module
https://www.digikey.dk/da/product-highlight/s/septentrio/mosaic-go-heading-gnss-module-evaluation-kit# ratatosk_gnss
