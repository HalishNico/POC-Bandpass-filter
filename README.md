# POC-Bandpass-filter
Python Project following the "intuitive" approach to digital filter design as described in Kuc Romans "Introduction to Digitler Signal Processing" 

# Theory 

# Intuitive Design Approach - Algorithm
The filter design this alogirthm uses is straight-forward and rudementary; add poles at frequencies that do not comply with the specifications of the passband. 

Initially, when the user gives the specifications of the passband, a pole is added in the middle frequency. For the stopband, zeroes are added at the middle and extremeties. 

Next, the frequency spectrum in decibels is checked for outliers within or just outside the passband, the most extreme outliers are tended to first. 

Poles are subsequently added starting from extremities of the passband, increasing in radius, and moving in towards the centre of the passband until the previously found outlier frequency is solved. This process continues until there no more frequencies in the passband that need to be fixed or the alogirithm under its limitation can no longer fix the outlier frequencies.

At the end of the process the program outputs the poles, zeroes and gain coefficient required to create the digital signal filter it designed. 
