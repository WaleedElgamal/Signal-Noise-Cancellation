from  scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd


#setting number of samples and frequency axis range
N = 3*1024
f = np.linspace(0,512,int(N/2))

t= np.linspace(0,3,12*1024)

#generating noise signal using random frequencies 
f_n = np.random.randint(0,512,2) 
noise = np.sin(2*np.pi*f_n[0]*t) + np.sin(2*np.pi*f_n[1]*t)



#array storing third octave frequencies
third_octave_freq = [196,146.83,196,246.93,196,146.83]
#array storing fourth octave frequencies
fourth_octave_freq = [392,493.88,261.63,293.66,392,493.88]
#array storing varying time intervals between notes
time_between_notes = [0.2,0.1,0.3,0.2,0.1]
#array storing the value of each note endpoint
end_point= [0.4,0.9,1.5,2,2.4,3]
#variable storing each note startpoint
i= 0
#final signal summing all song notes
x=0
#counter for endpoint and frequency arrays
n =0
#counter for time_between_notes array
l=0


##looping over the 3 second duration, each time creating two signals
##and summing them to the final signal
##updating counters and checking condition to exit the loop
while i<3 :
   x1=np.where(np.logical_and(t>=i,t<=end_point[n]),np.sin(2*np.pi*third_octave_freq[n]*t),0)
   x2=np.where(np.logical_and(t>=i,t<=end_point[n]),np.sin(2*np.pi*fourth_octave_freq[n]*t),0)
   x = x+x1+x2
   if l == 5:
       break
   i = (end_point[n]+time_between_notes[l])
   n = n+1
   l = l+1


#converting original time signal to frequency signal
x_f = fft(x)
x_f = 2/N * np.abs(x_f[0:int(N/2)])

#adding generated noise to original signal and getting its corresponding signal in frequency domain
x_n = x + noise
x_nf = fft(x_n)
x_nf = 2/N * np.abs(x_nf[0:int(N/2)])


#using array to store the noise frequencies founnd in the signal
f_found= np.arange(0,2)
#looping over the frequency range to find the noise frequencies and stroing them in the array
j =0
temp = 0 ;
maxAmplitude = np.ceil(max(x_f))
while j < f.size :
    if x_nf[j] >maxAmplitude :
        f_found[temp]=f[j]
        temp +=1
    j +=1
     
#rounding frequencies since we use integer values and then removing the noise to get the filtered signal
f_found[0] = np.round(f_found[0])
f_found[1] = np.round(f_found[1])
x_filtered  = x_n - ( np.sin(2*f_found[0]*np.pi*t)+np.sin(2*f_found[1]*np.pi*t) )

#converting filtered time signal to frequency signal
x_fil_fft = fft(x_filtered)
x_fil_fft = 2/N * np.abs(x_fil_fft[0:int(N/2)])


#plotting all grapghs
plt.subplot(3,2,1)
plt.plot(t,x)
plt.subplot(3,2,2)
plt.plot(f,x_f)
plt.subplot(3,2,3)
plt.plot(t,x_n)
plt.subplot(3,2,4)
plt.plot(f,x_nf)
plt.subplot(3,2,5)
plt.plot(t,x_filtered)
plt.subplot(3,2,6)
plt.plot(f,x_fil_fft)



sd.play(x_filtered,3*1024)




