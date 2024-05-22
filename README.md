# POC-Bandpass-filter
Python Project following the "intuitive approach" to digital filter design as described in Kuc Romans "Introduction to Digitler Signal Processing" 

# Theory 
The purpose of a digital filter is to let specific certain frequencies of an digitized input signal either pass through or get filtered out. Since the input signal is digitized, so to is the output signal, an example of an equation for a filter is of the form are of the form:

$`$ y \{ n \} = x\{n\} + x\{n-1\} + y\{n-1\}$`$

Addtionally, it can be insightful to evalute the transfer function of a digital filter, by applying a z-transformation, which in this case gives:

$$ H(z) = \frac{1+z^{-1}}{1-z^{-1}}$$

Where in this case the input z, is any complex number of magnitude 1, which represents a particular frequency, depending on the sampling frequency used on the original signal. The critical thing to understand from the above equation is how as $z^{-1}$ approaches values of 1, the denominator becomes small and the values of $H(z)$ increase. Equally, as $z^{-1}$ approaches values of -1 the numerator becomes small and the value the value of $H(z)$ approaches zero. The terms in the numerator of a transfer function are referred to as zeroes and the terms in the denominator are referred to as poles. 

The spectrum the filter induces can be best evaluated from graphing the magnitude of the transfer fucntion with respect to $z$. The following equation is useful for this process:

$$|H(z)|² = H(z)H(z*)$$

Hence for each pole and zero, the magnitude is evaluated as follows:

$$ (1-e^{j(-\omega - \theta)})(1-e^{j(-\omega + \theta)})$$

Where $\omega$ is the argument/frequency at which there is a pole/zero and $\theta$ is the argument of the input $z$. Furthermore evaluating, the loagarithmic magnitude responses can be fruitful to facilitate evaluating the change in the transfer function when a pole is added. 

<p align="center">
  <img src="/Plots/passband400_500.png">
</p>


# Intuitive Design Approach - Algorithm
The filter design this alogirthm uses is straight-forward and rudementary; add poles at frequencies that do not comply with the specifications of the passband. 

Initially, when the user gives the specifications of the passband, a pole is added in the middle frequency. For the stopband, zeroes are added at the middle and extremeties. 

Next, the frequency spectrum in decibels is checked for outliers within or just outside the passband, the most extreme outliers are tended to first. 

Poles are subsequently added starting from extremities of the passband, increasing in radius, and moving in towards the centre of the passband until the previously found outlier frequency is solved. This process continues until there no more frequencies in the passband that need to be fixed or the alogirithm under its limitation can no longer fix the outlier frequencies.


At the end of the process the program outputs the poles, zeroes and gain coefficient required to create the digital signal filter it designed. 

# Possible Improvements and Moving Forwards

+ Investigate possibility of resolving inconsistencies in the passband by adding zeroes
+ Write code in c that can use the output of the python script to construct functinoal digital filter following CCOS structure
