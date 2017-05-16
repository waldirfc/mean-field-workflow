# ODE system por single workflow with a paralelism with two tasks sharing one resource
import time
import sys

start_time = time.time()

eps = 10e-6

#NUMBER OF STATES (number of ODEs)
S = 12

#The results are better for small values 'rate_val_execution' (ex. 1)
allR = 500.0 					#rate of allocation for a single resource
rate_val_probability = 500.0 	#rate value for transitions of choice
rate_val_execution = 1.0		#rate value for executions

#QUANTITY OF RESOURCES
R1 = int(sys.argv[2])

#CAPACITY OF WORK FOR RESOURCES
Capacity_R1 = 40.0

#ACTIVITY AND REQUERIMENTS
A_R1 = 20.0
B_R1 = 10.0
C_R1 = 40.0
D_R1 = 40.0 / 3

#EXECUTION RATES FOR ACTIVITY AND REQUERIMENTS
execAR1 = (Capacity_R1/A_R1) * rate_val_execution
execBR1 = (Capacity_R1/B_R1) * rate_val_execution
execCR1 = (Capacity_R1/C_R1) * rate_val_execution
execDR1 = 3.0 #(Capacity_R1/D_R1) * rate_val_execution

Xor1 = 0.8 * rate_val_probability
Xor2 = 0.2 * rate_val_probability

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
	freeR1 = (R1 - (y[2]+y[4]+y[5]+y[7]+y[9]+y[11]))

	# waiting instances
	waitingR1 = y[1] + y[3] + y[6] + y[8] + y[10]
	if waitingR1 <= eps:
		waitingR1 = 1

	# proportions of waiting instances	
	p1 = y[1] / waitingR1
	p3 = y[3] / waitingR1
	p6 = y[6] / waitingR1
	p8 = y[8] / waitingR1
	p10 = y[10] / waitingR1

	'''
	f0  = -allR*p1*(min(y[0], freeR1)) - allR*p1*(min(y[0], freeR1)) + execBR1*y[3] + execAR1*y[6]
	f1  = -execAR1*y[1] + allR*p1*(min(y[0], freeR1))
	f2  = -allR*p2*(min(y[2], freeR1)) + execAR1*y[1]
	f3  = -execBR1*y[3] + allR*p2*(min(y[2], freeR1))
	f4  = -execBR1*y[4] + allR*p1*(min(y[0], freeR1))
	f5  = -allR*p3*(min(y[5], freeR1)) + execBR1*y[4]
	f6  = -execAR1*y[6] + allR*p3*(min(y[5], freeR1))
	'''

	min_wait_free_R1 = min(waitingR1, freeR1)

	f0  = -Xor1*y[0] - Xor2*y[0] + execBR1*y[4] + execAR1*y[7] + execDR1*y[11]
	f1  = -allR*p1*min_wait_free_R1 -allR*p1*min_wait_free_R1 + Xor1*y[0]
	f2  = -execAR1*y[2] + allR*p1*min_wait_free_R1
	f3  = -allR*p3*min_wait_free_R1 + execAR1*y[2]
	f4  = -execBR1*y[4] + allR*p3*min_wait_free_R1
	f5  = -execBR1*y[5] + allR*p1*min_wait_free_R1
	f6  = -allR*p6*min_wait_free_R1 + execBR1*y[5]
	f7  = -execAR1*y[7] + allR*p6*min_wait_free_R1
	f8  = -allR*p8*min_wait_free_R1 + Xor2*y[0]
	f9  = -execCR1*y[9] + allR*p8*min_wait_free_R1	
	f10  = -allR*p10*min_wait_free_R1 + execCR1*y[9]
	f11  = -execDR1*y[11] + allR*p10*min_wait_free_R1

	return [f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11]


import odespy
import numpy as np

# initial conditions
N = int(sys.argv[1])			# initial population

#'''
pmax = 3						# number of points
iterations = pmax * 10
y0 = [N, 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]		# initial condition vector
t  = np.linspace(0, pmax, iterations)	# time grid

solver = odespy.Lsode(f3)
solver.set_initial_condition(y0)
u, t = solver.solve(t)

print("Tempo = {} seg\n".format(time.time() - start_time))

for i in range(0, S):
	print u[iterations - 1, i]

#----- PLOT SIMULATION -----
import matplotlib.pyplot as plt
plt.plot(t, u[:, 0], 'g+:',
	 t, u[:, 1], 'k*-',	 	 
	 t, u[:, 2], 'g.-',
     t, u[:, 3], 'b--',
     t, u[:, 4], 'gs-',
     t, u[:, 5], 'r*-',
     t, u[:, 6], 'rs:',
	 t, u[:, 7], 'k*-',	 	 
	 t, u[:, 8], 'b.-',
     t, u[:, 9], 'b*:',
     t, u[:, 10], 'r+:',
     t, u[:, 11], 'k+-',
     t, R1 - (u[:, 2] + u[:, 4] + u[:, 5] + u[:, 7] + u[:, 9] + u[:, 11]), 'r--')
plt.xlabel('time')
plt.ylabel('population')
plt.legend(['X_P0', 'X_P1', 'X_P2', 'X_P3', 'X_P4', 'X_P5', 'X_P6', 'X_P7', 'X_P8', 'X_P9', 'X_P10', 'X_P11', 'X_R1'])
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