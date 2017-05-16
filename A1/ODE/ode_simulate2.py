import time
import sys

eps = 10e-6
start_time = time.time()

#NUMBER OF STATES (number of ODEs)
S = 4

#The results are better for small values 'rate_val_execution' (ex. 1)
allR = 500.0 					#rate of allocation for a single resource
rate_val_probability = 500.0 	#rate value for transitions of choice
rate_val_execution = 1.0		#rate value for executions

#QUANTITY OF RESOURCES
R1 = int(sys.argv[2])

#CAPACITY OF WORK FOR RESOURCES
Capacity_R1 = 40.0

#ACTIVITY AND REQUERIMENTS
A_R1 = 10.0
B_R1 = 20.0

#EXECUTION RATES FOR ACTIVITY AND REQUERIMENTS
execAR1 = (Capacity_R1/A_R1) * rate_val_execution
execBR1 = (Capacity_R1/B_R1) * rate_val_execution

# solve the system dy/dt = f(y, t)
def f(y, t):

	'''
	# first approach: choose all the population
	#ALLOCATION RATES FOR RESOURCES
	waitingR1 = max(y[1] + y[2] + y[6], 1) # and if I give 1 only if the sum is 0???
	waitingR2 = max(y[1] + y[2] + y[5], 1)
	waitingR3 = max(y[2], 1)

	allR1 = allR * (R1 - (y[3]+y[8]+y[10])) / waitingR1
	allR2 = allR * (R2 - (y[4]+y[7]+y[10])) / waitingR2
	allR3 = allR * (R3 - (y[9])) / waitingR3
	
	f1  = -Xor1*y[0] - Xor2*y[0] + execR2*y[7] + execR1*y[8] + execR3_1*y[9] + execR3_2*y[10]
	f2  = -allR1*y[1] - allR2*y[1] + Xor1*y[0]
	f3  = -allR3*y[2] - min(allR1, allR2)*y[2] + Xor2*y[0]
	f4  = -execR1*y[3] + allR1*y[1]
	f5  = -execR2*y[4] + allR2*y[1]
	f6  = -allR2*y[5] + execR1*y[3]
	f7  = -allR1*y[6] + execR2*y[4]
	f8  = -execR2*y[7] + allR2*y[5]
	f9  = -execR1*y[8] + allR1*y[6]
	f10 = -execR3_1*y[9] + allR3*y[2]
	f11 = -execR3_2*y[10] + min(allR1, allR2)*y[2]
	'''	
	# second approach: choose min between population and available resources
	L1 = ((R1 - (y[1] + y[3])))

	waitingR1 = y[0] + y[2]
	if waitingR1 <= eps:
		waitingR1 = 1

	proportion1 = y[0]/waitingR1
	proportion2 = y[2]/waitingR1
	
	f0  = -allR*proportion1*(min(waitingR1,L1)) + execBR1*y[3]
	f1  = -execAR1*y[1] + allR*proportion1*(min(waitingR1,L1))
	f2  = -allR*proportion2*(min(waitingR1,L1)) + execAR1*y[1]
	f3  = -execBR1*y[3] + allR*proportion2*(min(waitingR1,L1))

	print("----------------------------------------------------")
	print(t)
	print("{} \t {} \t {} \t {}".format(y[0], y[1], y[2], y[3]))
	print("{} \t {} \t {} \t {}".format(f0, f1, f2, f3))

	return [f0, f1, f2, f3]

import odespy
import numpy as np
import sys

# initial conditions
N = int(sys.argv[1])					# initial population
#'''
pmax = 3								# max time
iterations = pmax * 10					# number of iterations
y0 = [N, 0., 0., 0.]					# initial condition vector
t  = np.linspace(0, pmax, iterations)	# time grid


solver = odespy.Lsode(f)
solver.set_initial_condition(y0)
u, t = solver.solve(t)

print("Tempo = {} seg\n".format(time.time() - start_time))

P0 = u[:,0]
P1 = u[:,1]
P2 = u[:,2]
P3 = u[:,3]

#k = len(Xd)
#print Xd[k-1]+Xi[k-1]+Xl[k-1]
#print Xe[k-1]+Xh[k-1]+Xl[k-1]
#print Xk[k-1]
for i in range(0, S):
	print u[iterations - 1, i]

import matplotlib.pyplot as plt
plt.plot(t, P0, 'rs:',
	 t, P1, 'k*-',	 	 
	 t, P2, 'g.-',
     t, P3, 'bs',
     t, R1 - (P1 + P3), 'r--')
plt.xlabel('tempo')
plt.ylabel('fichas')
plt.legend(['X_P0', 'X_P1', 'X_P2', 'X_P3', 'X_R1'])
plt.savefig('ode-' + str(N) + "I-" + str(R1) + "R.pdf", bbox_inches='tight')
#show()
#'''

'''
# --- TEST VARIOUS INSTANCES ----

for i in range(1, N + 1):
	pmax = 60						# number of points
	y0 = [i, 0.]	# initial condition vector
	t  = np.linspace(0, pmax, pmax*2)	# time grid

	solver = odespy.Lsode(f)
	solver.set_initial_condition(y0)
	u, t = solver.solve(t)

	#print("{} INSTANCES".format(i))
	print("R1 utilization: {}".format(u[99,1]))
'''