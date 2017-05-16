# ODE system por single workflow with a paralelism with two tasks sharing one resource
import time
import sys

start_time = time.time()

eps = 10e-6

#NUMBER OF STATES (number of ODEs)
S = 7

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

# FIRST APPROACH: choose all the population, rate (free/waiting) ERRO
def f1(y, t):
	# free resources
	freeR1 = (R1 - (y[1]+y[3]+y[4]+y[6]))

	# waiting instances
	waitingR1 = y[0] + y[2] + y[5]
	if waitingR1 <= eps:
		waitingR1 = 1	
	
	# allocation rates for resources
	allR1 = (allR * freeR1) / waitingR1
	
	f0  = -allR1*(min(y[0], freeR1)) - allR1*(min(y[0], freeR1)) + execBR1*y[3] + execAR1*y[6]
	f1  = -execAR1*y[1] + allR1*(min(y[0], freeR1))
	f2  = -allR1*(min(y[2], freeR1)) + execAR1*y[1]
	f3  = -execBR1*y[3] + allR1*(min(y[2], freeR1))
	f4  = -execBR1*y[4] + allR1*(min(y[0], freeR1))
	f5  = -allR1*(min(y[5], freeR1)) + execBR1*y[4]
	f6  = -execAR1*y[6] + allR1*(min(y[5], freeR1))
	
	return [f0, f1, f2, f3, f4, f5, f6]	

# SECOND APPROACH: choose min between population and available resources (min(y[i], free))	
def f2(y, t):
	# free resources
	freeR1 = (R1 - (y[1]+y[3]+y[4]+y[6]))

	# waiting instances
	waitingR1 = y[0] + y[2] + y[5]
	if waitingR1 <= eps:
		waitingR1 = 1

	f0  = -allR*(min(y[0], freeR1)) - allR*(min(y[0], freeR1)) + execBR1*y[3] + execAR1*y[6]
	f1  = -execAR1*y[1] + allR*(min(y[0], freeR1))
	f2  = -allR*(min(y[2], freeR1)) + execAR1*y[1]
	f3  = -execBR1*y[3] + allR*(min(y[2], freeR1))
	f4  = -execBR1*y[4] + allR*(min(y[0], freeR1))
	f5  = -allR*(min(y[5], freeR1)) + execBR1*y[4]
	f6  = -execAR1*y[6] + allR*(min(y[5], freeR1))

	return [f0, f1, f2, f3, f4, f5, f6]

# THRID APPROACH: proportions between waiting states (y[i]/waiting)
def f3(y, t):
	# free resources
	freeR1 = (R1 - (y[1]+y[3]+y[4]+y[6]))

	# waiting instances
	waitingR1 = y[0] + y[2] + y[5]
	if waitingR1 <= eps:
		waitingR1 = 1

	# proportions of waiting instances	
	p1 = y[0] / waitingR1
	p2 = y[2] / waitingR1
	p3 = y[5] / waitingR1

	'''
	f0  = -allR*p1*(min(y[0], freeR1)) - allR*p1*(min(y[0], freeR1)) + execBR1*y[3] + execAR1*y[6]
	f1  = -execAR1*y[1] + allR*p1*(min(y[0], freeR1))
	f2  = -allR*p2*(min(y[2], freeR1)) + execAR1*y[1]
	f3  = -execBR1*y[3] + allR*p2*(min(y[2], freeR1))
	f4  = -execBR1*y[4] + allR*p1*(min(y[0], freeR1))
	f5  = -allR*p3*(min(y[5], freeR1)) + execBR1*y[4]
	f6  = -execAR1*y[6] + allR*p3*(min(y[5], freeR1))
	'''

	f0  = -allR*p1*(min(waitingR1, freeR1)) - allR*p1*(min(waitingR1, freeR1)) + execBR1*y[3] + execAR1*y[6]
	f1  = -execAR1*y[1] + allR*p1*(min(waitingR1, freeR1))
	f2  = -allR*p2*(min(waitingR1, freeR1)) + execAR1*y[1]
	f3  = -execBR1*y[3] + allR*p2*(min(waitingR1, freeR1))
	f4  = -execBR1*y[4] + allR*p1*(min(waitingR1, freeR1))
	f5  = -allR*p3*(min(waitingR1, freeR1)) + execBR1*y[4]
	f6  = -execAR1*y[6] + allR*p3*(min(waitingR1, freeR1))

	return [f0, f1, f2, f3, f4, f5, f6]


import odespy
import numpy as np

# initial conditions
N = int(sys.argv[1])			# initial population

#'''
pmax = 3						# number of points
iterations = pmax * 10
y0 = [N, 0., 0., 0., 0., 0., 0.]		# initial condition vector
t  = np.linspace(0, pmax, iterations)	# time grid

solver = odespy.Lsode(f3)
solver.set_initial_condition(y0)
u, t = solver.solve(t)

print("Tempo = {} seg\n".format(time.time() - start_time))

for i in range(0, S):
	print u[iterations - 1, i]

#----- PLOT SIMULATION -----
import matplotlib.pyplot as plt
plt.plot(t, u[:, 0], 'gs:',
	 t, u[:, 1], 'ks-',	 	 
	 t, u[:, 2], 'bp-',
     t, u[:, 3], 'g*:',
     t, u[:, 4], 'r,:',
     t, u[:, 5], 'kh:',
     t, u[:, 6], 'r+:',
     t, R1 - (u[:, 1] + u[:, 3] + u[:, 4] + u[:, 6]), 'b--')
plt.xlabel('tempo')
plt.ylabel('fichas')
plt.legend(['X_P0', 'X_P1', 'X_P2', 'X_P3', 'X_P4', 'X_P5', 'X_P6', 'X_R1'])
plt.savefig('ode-I' + str(N) + '-R' + str(R1) + '.pdf', bbox_inches='tight')

'''

# --- TEST VARIOUS INSTANCES ----

for i in range(10, N + 1):
	pmax = 60							# number of points
	y0 = [i, 0., 0., 0., 0., 0., 0.]	# initial condition vector
	t  = np.linspace(0, pmax, pmax*2)	# time grid

	solver = odespy.Lsode(f2)
	solver.set_initial_condition(y0)
	u, t = solver.solve(t)

	print("{} INSTANCES".format(i))
	print("R1 utilization: {}".format(u[99,1]+u[99,3]+u[99,4]+u[99,6]))
	for j in range(0, 7):
		print u[99, j]
'''