# --- Population Continuous Time Markov Chain for the BPMN paper model ---
import numpy as np
import time
import sys

Nstates = 5 #number of states

start_time = time.time()

N = int(sys.argv[1])

iterations = 10 * N + 1

#The results are better for small values 'rate_val_execution' (ex. 1)
allR = 50.0 					#rate of allocation for a single resource
rate_val_probability = 50.0 	#rate value for transitions of choice
rate_val_execution = 1.0		#rate value for executions

#QUANTITY OF RESOURCES
R1 = 10.0

#CAPACITY OF WORK FOR RESOURCES
Capacity_R1 = 10.0

#ACTIVITY AND REQUERIMENTS
A_R1 = 30.0
B_R1 = 20.0

#EXECUTION RATES FOR ACTIVITY AND REQUERIMENTS
execR1A = (Capacity_R1/A_R1) * rate_val_execution
execR1B = (Capacity_R1/B_R1) * rate_val_execution

Xor1 = 0.40 * rate_val_probability
Xor2 = 0.60 * rate_val_probability

# --- REPEAT GILLESPIE SIMULATION X TIMES ---
simulations = 1000

S = np.zeros((iterations, Nstates))
S[0, 0] = N
t = [0]

for simulation in range(0, simulations):

	# Initial conditions
	x = np.zeros((iterations, Nstates))
	x[0, 0] = N

	trate = np.zeros(8)

	t = np.zeros(iterations)
	k = 0

	while k < iterations - 1:

		L1 = R1 - (x[k, 2] + x[k, 4])

		allR1 = allR * min(1, max(L1, 0)) # allocate if there is at least one available resource
		
		trate[0] = Xor1 * x[k, 0] #a->b
		trate[1] = allR1 * min(L1, x[k, 1]) #b->c
		trate[2] = execR1A * x[k, 2] #c->a
		trate[3] = Xor2 * x[k, 0] #a->d
		trate[4] = allR1 * min(L1, x[k, 3]) #d->e
		trate[5] = execR1B * x[k, 4] #e->a

		trate = np.cumsum(trate)

		tTotal = trate[5]

		k = k + 1

		# population update	
		x[k, :] = x[k - 1, :]

		# next time step
		exp_time = np.random.exponential(1/tTotal)
		t[k] = t[k - 1] + exp_time

		# simulate next transition
		next_transition = np.random.random()		

		if next_transition < (trate[0] / tTotal):
			x[k, 0] = x[k, 0] - 1
			x[k, 1] = x[k, 1] + 1
		elif next_transition < (trate[1] / tTotal):
			x[k, 1] = x[k, 1] - 1
			x[k, 2] = x[k, 2] + 1
		elif next_transition < (trate[2] / tTotal):
			x[k, 2] = x[k, 2] - 1
			x[k, 0] = x[k, 0] + 1
		elif next_transition < (trate[3] / tTotal):
			x[k, 0] = x[k, 0] - 1
			x[k, 3] = x[k, 3] + 1
		elif next_transition < (trate[4] / tTotal):
			x[k, 3] = x[k, 3] - 1
			x[k, 4] = x[k, 4] + 1
		else:
			x[k, 4] = x[k, 4] - 1
			x[k, 0] = x[k, 0] + 1

	S = S + x

S = S / simulations
print("Tempo = {}\n ({} simulations - {} iterations - {} max time)\n".format(time.time() - start_time, simulations, iterations, t[iterations - 1]))

np.savetxt('pctmc-' + str(N) + 'i-10r.results', S, delimiter=' ', fmt='%f')
for i in range(0, Nstates):
	print('{}'.format(S[iterations - 1, i]))

print('R1 utilization = {}'.format(S[iterations-1,2] + S[iterations-1,4]))

#resultado = [t(:) x']
#save gillespie_bpmn_10000.gnu resultado
#last_state = x[k, :)
#save gillespie_bpmn_ultimo_10000.gnu last_state

#----- PLOT SIMULATION -----
from matplotlib.pyplot import *
plot(t, S[:, 0], 'k-',
     t, S[:, 1], 'r*-',
     t, S[:, 2], 'gs-',
     t, S[:, 3], 'kd-',
     t, S[:, 4], 'b--')
legend(['Xa', 'Xb', 'Xc', 'Xd', 'Xe'])
savefig('pctmc-' + str(N) + "i-10r.pdf", bbox_inches='tight')
#show()
