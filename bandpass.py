import math
import matplotlib.pyplot as plt

#class which holds values relevant to the filter design for conveneince 
class singularities:
    poles= []
    zeroes= []
    poles_radius= []
    poles_coef= []
    zeroes_coef= []
    epsilon= float
    passband=[]
    stopband=[]
    spec= int
    rcoef=int

#Values that are relevant to the plotting of poles and accuracy of results
resolution=130
repeats=2 

def singularities_calc():
    transfer = singularities()
    transfer.rcoef=1    
    ws = int(input("sampling frequency?(Hz) :"))
    transfer.epsilon=1
    transfer.spec=-20
    transfer.passband = []
    transfer.stopband = []

    transfer.passband.append(input("passband lower bound? : \n"))
    transfer.passband.append(input("passband upper bound? : \n"))

    transfer.stopband.append(input("stopband lower bound? : \n"))
    transfer.stopband.append(input("stopband upper bound? : \n"))

    other_p = (input("extra stopband? (Y/N)\n")).lower()
    if(other_p != "n"):
        print("stopband lower bounder : " + other_p)
        transfer.stopband.append(other_p)
        transfer.stopband.append(input("stopband upper bound? : \n"))

    for i in range(len(transfer.passband)):
        transfer.passband[i]=(2*math.pi*int(transfer.passband[i])/(ws))
    for i in range(len(transfer.stopband)):
        transfer.stopband[i]=(2*math.pi*int(transfer.stopband[i])/(ws))

    if(transfer.passband[0] == 0):
        transfer.passband[0] = -transfer.passband[1]
    elif(transfer.passband[1] == math.pi):
        transfer.passband[1] = 2*math.pi-transfer.passband[0] 

    radius=0.7
    peak=0.5*(transfer.passband[1]+ transfer.passband[0])
    print("peak" + str(peak))
    transfer.poles.append(peak)
    if(peak%math.pi!=0):
        transfer.poles_coef.append((radius, math.cos(peak), 2))
    else:
        transfer.poles_coef.append((radius, math.cos(peak), 1))
    transfer.poles_radius.append(radius)
    
    counter=0
    while(counter<len(transfer.stopband)):
        if(transfer.stopband[counter] == 0):
            transfer.stopband[counter] = -transfer.stopband[counter+1]
        elif(transfer.stopband[counter + 1] == math.pi):
            transfer.stopband[counter + 1] = 2*math.pi-transfer.stopband[counter] 
        trough= 0.5*(transfer.stopband[counter+1] + transfer.stopband[counter])
        transfer.zeroes.append(trough)
        transfer.zeroes.append(transfer.stopband[counter])
        transfer.zeroes.append(transfer.stopband[counter+1])
        counter+=2
    
    for i in range(len(transfer.zeroes)):
        if((transfer.zeroes[i] <0.01 and transfer.zeroes[i] > -0.01) or (transfer.zeroes[i] <math.pi + 0.01 and transfer.zeroes[i] > math.pi-0.01)):
            transfer.zeroes_coef.append((0.96, math.cos(transfer.zeroes[i]), 1))
        else:
            transfer.zeroes_coef.append( (0.96, math.cos(transfer.zeroes[i]), 2))
    
    transfer.poles_coef = list(dict.fromkeys(transfer.poles_coef))
    transfer.zeroes_coef = list(dict.fromkeys(transfer.zeroes_coef))
    htot, wz, transfer.rcoef = filter_make(transfer)
    plt.plot(wz, htot)
    plt.axvline(x = transfer.passband[1], color = 'b', label = 'axvline - full height')
    plt.axvline(x = transfer.passband[0], color = 'b', label = 'axvline - full height')
    plt.show()
    print("\n")
    if(input("Add poles to improve the design? (Y/N)\n").lower()=="y"):
        transfer = fix(transfer)
    htot, wz, transfer.rcoef = filter_make(transfer)
    plt.plot(wz, htot, marker="x", color="r")
    plt.axvline(x = transfer.passband[1], color = 'b', label = 'axvline - full height')
    plt.axvline(x = transfer.passband[0], color = 'b', label = 'axvline - full height')
    plt.show()


def fix(transfer):
    htot_tot=[]
    boo, freq_fix= passband_check(transfer)
    #This is just the middle of the passband
    primal_peak = 0.5*(transfer.passband[0] + transfer.passband[1])
    htot, wz, transfer.rcoef= filter_make(transfer)
    while(boo):
        peak=transfer.passband[0] - (math.pi/20)
        while(htot[freq_fix] < max(htot) - transfer.epsilon):
            print("freq_fix:")
            print(wz[freq_fix] * (500/math.pi))
            for r in range(30, 97):
                radius=r/100
                if(peak%math.pi!=0):
                    htot_pr, zz, rp= pole_view(( radius, math.cos(peak), 2))
                else:
                    htot_pr, zz, rp= pole_view(( radius, math.cos(peak), 1))
                peak_n= 2*primal_peak -peak
                if(peak_n%math.pi!=0):
                    htot_pl, zz, rp= pole_view(( radius, math.cos(peak_n), 2))
                else:
                    htot_pl, zz, rp= pole_view(( radius, math.cos(peak_n), 1))
                #To re evalute, potentially causing issues relating
                #to adding two points of actually different times
                n=len(htot)
                for m in range(n):
                    try:
                        htot_tot[m]=htot[m]+htot_pr[m] + htot_pl[m]
                    except:
                        htot_tot.append(htot[m]+htot_pr[m] + htot_pl[m])
                htot_tot_max =max(htot_tot)
                if(htot_tot[freq_fix] >= htot_tot_max - transfer.epsilon):
                    transfer.poles.append(peak)
                    if(peak%math.pi!=0):
                        transfer.poles_coef.append((radius, math.cos(peak), 2))
                    else:
                        transfer.poles_coef.append((radius, math.cos(peak), 1))
                    if(peak_n%math.pi!=0):
                        transfer.poles_coef.append((radius, math.cos(peak_n), 2))
                    else:
                        transfer.poles_coef.append((radius, math.cos(peak_n), 1))
                    htot, wz, transfer.rcoef= filter_make(transfer)

                    print(htot[freq_fix])
                    plt.plot(wz, htot, marker="x")
                    plt.axvline(x = wz[freq_fix], color = 'b', label = 'axvline - full height')
                    plt.axvline(x = transfer.passband[1], color = 'b', label = 'axvline - full height')
                    plt.axvline(x = transfer.passband[0], color = 'b', label = 'axvline - full height')
                    plt.show()
                    print("This is the graph once a new pole was added")
                    if(input("continue adding poles? Y/N").lower() == "n"):
                        return transfer
                    print(max(htot))
                    print(transfer.rcoef)
                    break
            peak=peak+(math.pi/180)
            if(peak>primal_peak):#To modify this code later if needed, might need to make it w_s/2 
                print("The alogorithm reached a point whereby it can no longer improve the filter design")
                return transfer
        boo,freq_fix = passband_check(transfer)
        htot, wz, transfer.rcoef= filter_make(transfer)
    return transfer

#Returns a True and the frequency that does not conform to the passband specifications,
#and False if the passband specifications have been met 
def passband_check(transfer):
    htot, wz, transfer.rcoef = filter_make(transfer)
    hmax = max(htot)
    n=len(wz)
    freq=[]
    #Only the LHS of the passband checked, as any values that are later corrected
    #by adding pole, an additional pole will be added on the opposite side of the passband 
    for i in range(n):
        if(wz[i] >= transfer.passband[0] and wz[i] <= 0.5*(transfer.passband[0]+transfer.passband[1])):
            if(htot[i] < hmax-transfer.epsilon):
                freq.append(( hmax-htot[i], i))
        #This second check is if the first value outside of the passband is small enough
        #such that in a continuous frequency passband, the edges of the passband are up to
        #specification
        elif(i<n-1 and wz[i+1] >= transfer.passband[0] and wz[i+1] <= 0.5*(transfer.passband[0]+transfer.passband[1])):
            if( htot[i+1]-  (wz[i+1] - transfer.passband[0])*(htot[i+1]-htot[i])/(wz[i+1] - wz[i]) < hmax-transfer.epsilon ):
                freq.append(( hmax-htot[i+1]-(wz[i+1]-transfer.passband[0])*(htot[i+1]-htot[i])/(wz[i+1]-wz[i]), i))
    if(len(freq)!=0):
        fm=0
        ii=0
        for f in freq:
            if(f[0] >fm):
                ii=f[1]
                fm=f[0]
        return True, ii
    else:
        return False, -1    

#This filter plots the magnitude of the filter in decibels, using some equations
#derived from multiplying the transfer function in the z-domain by its conjugate
def filter_make(transfer):
    htot=[]
    wz=[]
    for z in range(resolution):
        numerator=1
        denominator=1
        w = (repeats*z*math.pi)/resolution
        for n in transfer.poles_coef:
            #n[0] is the radiusof the pole  and n[1] is cosine of its argument
            if(n[2] == 2):
                denominator=denominator*(1  - (4/n[0])*n[1]*math.cos(w) + (2/(n[0]**2))*math.cos(2*w)+(4/(n[0]**2))*n[1]*n[1] - (4/(n[0]**3))*n[1]*math.cos(w)+(1/(n[0]**4)) )
            else:
                denominator=denominator*(1-(2*n[1]/n[0])*math.cos(w)+1/(n[0]**2))
        for n in transfer.zeroes_coef:
            if(n[2] == 2):
                numerator=numerator*(1  - (4/n[0])*n[1]*math.cos(w) + (2/(n[0]**2))*math.cos(2*w)+(4/(n[0]**2))*n[1]*n[1] - (4/(n[0]**3))*n[1]*math.cos(w)+(1/(n[0]**4)) )
            else:
                numerator=numerator*(1-(2*n[1]/n[0])*math.cos(w)+1/(n[0]**2))
        if(numerator*denominator>0):
            htot.append(10*math.log10(numerator/denominator))
            wz.append(w)
    hmax=max(htot)
    if(hmax>0):
        hmax=-hmax
    for i in range(len(htot)):
        htot[i] = htot[i]+hmax
    rcoef = transfer.rcoef*math.pow(10, hmax/20)
    return htot, wz, rcoef

def pole_view(n):
    htot=[]
    wz=[]
    for z in range(resolution):
        w = (repeats*z*math.pi)/resolution
        numerator=1
        if(n[2] == 2):
            numerator=numerator*(1  - (4/n[0])*n[1]*math.       cos(w) + (2/(n[0]**2))*math.cos(2*w)+(4/(n[0]**2))*n[1]*n[1] - (4/(n[0]**3))*n[1]*math.cos(w)+(1/(n[0]**4)) )
        else:
            numerator=numerator*(1-(2*n[1]/n[0])*math.cos(w)+1/(n[0]**2))
        if(numerator!=0):
            htot.append(10*math.log10(1/numerator))
            wz.append(w)
    hmin=-min(htot)
    for i in range(len(htot)):
        htot[i] = htot[i]+hmin
    rmin = math.pow(10, hmin/20)
    return htot, wz, rmin

singularities_calc()