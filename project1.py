import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd


t= np.linspace(0,3,12*1024)

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
add=0
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
   add = add+x1+x2
   if l == 5:
       break
   i = (end_point[n]+time_between_notes[l])
   n = n+1
   l = l+1

plt.plot(t,add)
sd.play(add,3*1024)




