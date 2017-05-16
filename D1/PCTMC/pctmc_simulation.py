# --- Population Continuous Time Markov Chain for the BPMN paper model ---
import numpy as np
import time
import sys

start_time = time.time()

N = int(sys.argv[1])

iterations = 100 * N

#The results are better for small values 'rate_val_execution' (ex. 1)
allR = 50.0 					#rate of allocation for a single resource
rate_val_probability = 50.0 	#rate value for transitions of choice
rate_val_execution = 1.0		#rate value for executions

#QUANTITY OF RESOURCES
R1 = 2.0
R2 = 2.0
R3 = 2.0

#CAPACITY OF WORK FOR RESOURCES
Capacity_R1 = 5.0
Capacity_R2 = 6.0
Capacity_R3 = 8.0

#ACTIVITY AND REQUERIMENTS
A_R1 = 20.0
B_R2 = 10.0
C_R3 = 5.0
C_R1 = 10.0
C_R2 = 4.0

#EXECUTION RATES FOR ACTIVITY AND REQUERIMENTS
execR1 = (Capacity_R1/A_R1) * rate_val_execution
execR2 = (Capacity_R2/B_R2) * rate_val_execution
execR3_1 = (Capacity_R3/C_R3) * rate_val_execution
execR3_2 = min(Capacity_R1/C_R1, Capacity_R2/C_R2) * rate_val_execution

Xor1 = 0.35 * rate_val_probability
Xor2 = 0.65 * rate_val_probability

# --- REPEAT GILLESPIE SIMULATION X TIMES ---
simulations = 1000

S = np.zeros((iterations, 11))
S[0, 0] = N
t = [0]

for simulation in range(0, simulations):

	# Initial conditions
	x = np.zeros((iterations, 11))
	x[0, 0] = N

	trate = np.zeros(14)

	t = np.zeros(iterations)
	k = 0

	while k < iterations - 1:

		L1 = R1 - (x[k, 3] + x[k, 8] + x[k, 10])
		L2 = R2 - (x[k, 4] + x[k, 7] + x[k, 10])
		L3 = R3 - (x[k, 9])

		allR1 = allR * min(1, max(L1, 0)) # allocate if there is at least one available resource
		allR2 = allR * min(1, max(L2, 0))
		allR3 = allR * min(1, max(L3, 0))

		trate[0] = Xor1 * x[k, 0] #a->b
		trate[1] = Xor2 * x[k, 0] #a->c
		trate[2] = allR1 * min(L1, x[k, 1]) #b->d
		trate[3] = allR2 * min(L2, x[k, 1]) #b->e
		trate[4] = allR3 * min(L3, x[k, 2]) #c->k
		trate[5] = min(allR1, allR2) * min(min(L1, L2), x[k, 2]) #c->l
		trate[6] = execR1 * x[k, 3] #d->f
		trate[7] = execR2 * x[k, 4] #e->g
		trate[8] = allR2 * min(L2, x[k, 5]) #f->h
		trate[9] = allR1 * min(L1, x[k, 6]) #g->i
		trate[10] = execR2 * x[k, 7] #h->a
		trate[11] = execR1 * x[k, 8] #i->a
		trate[12] = execR3_1 * x[k, 9] #k->a
		trate[13] = execR3_2 * x[k, 10] #l->a

		trate = np.cumsum(trate)

		tTotal = trate[13]

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
			x[k, 0] = x[k, 0] - 1
			x[k, 2] = x[k, 2] + 1
		elif next_transition < (trate[2] / tTotal):
			x[k, 1] = x[k, 1] - 1
			x[k, 3] = x[k, 3] + 1
		elif next_transition < (trate[3] / tTotal):
			x[k, 1] = x[k, 1] - 1
			x[k, 4] = x[k, 4] + 1
		elif next_transition < (trate[4] / tTotal):
			x[k, 2] = x[k, 2] - 1
			x[k, 9] = x[k, 9] + 1
		elif next_transition < (trate[5] / tTotal):
			x[k, 2] = x[k, 2] - 1
			x[k, 10] = x[k, 10] + 1
		elif next_transition < (trate[6] / tTotal):
			x[k, 3] = x[k, 3] - 1
			x[k, 5] = x[k, 5] + 1
		elif next_transition < (trate[7] / tTotal):
			x[k, 4] = x[k, 4] - 1
			x[k, 6] = x[k, 6] + 1
		elif next_transition < (trate[8] / tTotal):
			x[k, 5] = x[k, 5] - 1
			x[k, 7] = x[k, 7] + 1
		elif next_transition < (trate[9] / tTotal):
			x[k, 6] = x[k, 6] - 1
			x[k, 8] = x[k, 8] + 1
		elif next_transition < (trate[10] / tTotal):
			x[k, 7] = x[k, 7] - 1
			x[k, 0] = x[k, 0] + 1
		elif next_transition < (trate[11] / tTotal):
			x[k, 8] = x[k, 8] - 1
			x[k, 0] = x[k, 0] + 1
		elif next_transition < (trate[12] / tTotal):
			x[k, 9] = x[k, 9] - 1
			x[k, 0] = x[k, 0] + 1
		else:
			x[k, 10] = x[k, 10] - 1
			x[k, 0] = x[k, 0] + 1

	S = S + x

S = S / simulations
print("Tempo = {}\n ({} simulations - {} iterations - {} max time)\n".format(time.time() - start_time, simulations, iterations, t[iterations - 1]))

np.savetxt('pctmc-' + str(N) + 'i-2r.results', S, delimiter=' ', fmt='%f')
for i in range(0, 11):
	print('{}'.format(S[iterations - 1, i]))

print('R1 utilization = {}'.format(S[iterations-1,3]+S[iterations-1,8]+S[iterations-1,10]))
print('R2 utilization = {}'.format(S[iterations-1,4]+S[iterations-1,7]+S[iterations-1,10]))
print('R3 utilization = {}'.format(S[iterations-1,9]))

#resultado = [t(:) x']
#save gillespie_bpmn_10000.gnu resultado
#last_state = x[k, :)
#save gillespie_bpmn_ultimo_10000.gnu last_state

#----- PLOT SIMULATION -----
from matplotlib.pyplot import *
plot(t, S[:, 0], 'k-',
     t, S[:, 1], 'b--',
     t, S[:, 2], 'g-',
     t, S[:, 3], 'r*-',
     t, S[:, 4], 'rs-',
     t, S[:, 5], 'r-',
     t, S[:, 6], 'k.-',
     t, S[:, 7], 'bs-',
     t, S[:, 8], 'b*-',     
     t, S[:, 9], 'rd-',
     t, S[:, 10], 'go--')
legend(['Xa', 'Xb', 'Xc', 'Xd', 'Xe', 'Xf', 'Xg', 'Xh', 'Xi', 'Xk', 'Xl'])
savefig('pctmc-' + str(N) + 'i-2r.pdf', bbox_inches='tight')
#show()
