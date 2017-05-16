import time
import sys

start_time = time.time()

#NUMBER OF STATES (number of ODEs)
S = 5

eps = 10e-6

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
execR1A = (Capacity_R1/A_R1) * rate_val_execution
execR1B = (Capacity_R1/B_R1) * rate_val_execution

Xor1 = 0.8 * rate_val_probability
Xor2 = 0.2 * rate_val_probability

# solve the system dy/dt = f(y, t)

# FIRST APPROACH: choose all the population, rate (free/waiting) ERRO
def f1(y, t):
	# free resources
	freeR1 = (R1 - (y[2]+y[4]))

	# instances waiting for resource
	waitingR1 = y[1] + y[3]
	if waitingR1 <= eps:
		waitingR1 = 1
	
	# allocation rates for resources
	allR1 = (allR * freeR1) / waitingR1
	
	f0  = -Xor1*y[0] - Xor2*y[0] + execR1A*y[2] + execR1B*y[4]
	f1  = -allR1*(min(y[1], freeR1)) + Xor1*y[0]
	f2  = -execR1A*y[2] + allR1*(min(y[1], freeR1))
	f3  = -allR1*(min(y[3], freeR1)) + Xor2*y[0]
	f4  = -execR1B*y[4] + allR1*(min(y[3], freeR1))
	
	return [f0, f1, f2, f3, f4]

# SECOND APPROACH: choose min between population and available resources (min(y[i], free))
def f2(y, t):
	# free resources
	freeR1 = (R1 - (y[2]+y[4]))

	# instances waiting for resource
	waitingR1 = y[1] + y[3]
	if waitingR1 <= eps:
		waitingR1 = 1

	f0  = -Xor1*y[0] - Xor2*y[0] + execR1A*y[2] + execR1B*y[4]
	f1  = -allR*(min(y[1], freeR1)) + Xor1*y[0]
	f2  = -execR1A*y[2] + allR*(min(y[1], freeR1))
	f3  = -allR*(min(y[3], freeR1)) + Xor2*y[0]
	f4  = -execR1B*y[4] + allR*(min(y[3], freeR1))

	return [f0, f1, f2, f3, f4]

# THRID APPROACH: proportions between waiting states (y[i]/waiting)
# test choice, try pulling states or multiply final rates???????????
def f3(y, t):
	# free resources
	freeR1 = (R1 - (y[2]+y[4]))

	# instances waiting for resource
	waitingR1 = y[1] + y[3]
	if waitingR1 <= eps:
		waitingR1 = 1

	# proportions of waiting instances	
	p1 = (y[1] / waitingR1) #* execR1B * Xor2
	p2 = (y[3] / waitingR1) #* execR1A * Xor1

	f0  = -Xor1*y[0] - Xor2*y[0] + execR1A*y[2] + execR1B*y[4]
	# f1  = -allR*p1*min(y[1], freeR1) + Xor1*y[0]
	# f2  = -execR1A*y[2] + allR*p1*min(y[1], freeR1)
	# f3  = -allR*p2*min(y[3], freeR1) + Xor2*y[0]
	# f4  = -execR1B*y[4] + allR*p2*min(y[3], freeR1)
	f1  = -allR*p1*min(waitingR1, freeR1) + Xor1*y[0]
	f2  = -execR1A*y[2] + allR*p1*min(waitingR1, freeR1)
	f3  = -allR*p2*min(waitingR1, freeR1) + Xor2*y[0]
	f4  = -execR1B*y[4] + allR*p2*min(waitingR1, freeR1)

	return [f0, f1, f2, f3, f4]


import odespy
import numpy as np

# initial conditions
N = int(sys.argv[1])			# initial population

#'''
pmax = 3						# number of points
iterations = pmax * 10
y0 = [N, 0., 0., 0., 0.]	# initial condition vector
t  = np.linspace(0, pmax, iterations)	# time grid

solver = odespy.Lsode(f3)
solver.set_initial_condition(y0)
u, t = solver.solve(t)

print("Tempo = {} seg\n".format(time.time() - start_time))

Xa = u[:,0]
Xb = u[:,1]
Xc = u[:,2]
Xd = u[:,3]
Xe = u[:,4]

for i in range(0, S):
	print u[iterations - 1, i]

#----- PLOT SIMULATION -----
import matplotlib.pyplot as plt
plt.plot(t, u[:, 0], 'gs:',
	 t, u[:, 1], 'k*-',	 	 
	 t, u[:, 2], 'g.-',
     t, u[:, 3], 'bs',
     t, u[:, 4], 'rs',
     t, R1 - (u[:, 2] + u[:, 4]), 'r--')
plt.xlabel('tempo')
plt.ylabel('fichas')
plt.legend(['X_P0', 'X_P1', 'X_P2', 'X_P3', 'X_P4', 'X_R1'])
plt.savefig('ode-I' + str(N) + '-R' + str(R1) + '.pdf', bbox_inches='tight')

#'''

'''
# --- TEST VARIOUS INSTANCES ----

for i in range(10, N + 1):
	pmax = 60						# number of points
	y0 = [i, 0., 0., 0., 0.]	# initial condition vector
	t  = np.linspace(0, pmax, pmax*2)	# time grid

	solver = odespy.Lsode(f2)
	solver.set_initial_condition(y0)
	u, t = solver.solve(t)

	print("{} INSTANCES".format(i))
	print("R1 utilization: {}".format(u[99,2]+u[99,4]))
	print("{}\t{}\t{}\t{}\t{}".format(u[99,0], u[99,1], u[99,2], u[99,3], u[99,4]))
	#print(u[99,0])
'''