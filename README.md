# Quorum Sensing
This is the program that simulate quorum sensing (signaling for microorganism for the change of their population). This case, we want to estimate number of population by using algorithm as followed

## Algorithm (not in algorithmic language)
Let say we have a grid of size `w*h` which all of the grid cell has an agent (things that we want to count) occupied on (that is, `w*h` agents). The agent has two stages: *susceptible* and *refractory*. We initialize all of them on *susceptible* stage. For each time step, each agent has the probability `p` to say "Hey, I'm alive" or something similar to their neighbor (4 or 8) and they can only do it for itself one time. However, their neighbor also will say "Hey, someone say they are alive" (and its internal size count increase one) if it heard someone say something. Sadly, they have a bad vocal cord (let say that agent has one) so they need to rest for refractory time `R`. During this time, the agent is marked as *refractory* i.e. inert to any signal. The simulation end if no one say anything for quite a while (this case, `1/p`).    

## Bug
Yes, it is buggy. It might not converge sometimes but it is limited to 10000 iterations (hard-coded) so the number might jump high but guarantee to converge to something. Can change easily but note that the program will not ask you about that parameter. It is just a plainly bad implementation and hard to use estimator after all.

## How to run the program:
  - Dependencies
	  - Python 3.7.9 
	  - numpy 1.19.2 [Installed on pip]
  - open your terminal at the directory of this program (make sure that this python file is in the empty folder as it will generate some files) then type 
	  ```
    python3 ./quorum_sensing.py
    ```
    and follow the instruction on the screen. The result will print out in terminal (or stdout if you redirect it to grep or some other program) that will print out the estimated number of quorum (which is `w*h`) and the error of estimator. 
