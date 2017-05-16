# ---------------------------------------
#        MICROSCOPIC TRAJECTORIES
# ---------------------------------------

import shlex, subprocess, time
import numpy as np
import sys

S = 5	#number of states
Nplaces = 6 + 1		#number of places of the petri net (considering resources) + 1

N = sys.argv[1]
R = sys.argv[2]
file = open('microscopic-I' + N + '-R' + R + '.results', 'w+')

#----- COMMAND DSPN -----
cmdTransient = 'sudo /home/edisone/Documents/research/GreatSPN/DSPN-Tool-Release -load /home/edisone/Documents/research/GreatSPN/nets/MacroscopicTests/macroscopic.PNPRO.solution/GSPNC1 -epsilon 1.0E-7 -on-the-fly -i -i-power -rpar AR1 4.0 -rpar BR1 2.0 -mpar I 1 -mpar NR1 2 -rpar pr1 400.0 -rpar pr2 100.0 -rpar r 500.0 -t 2 -all-measures'
cmdSteady = 'sudo /home/edisone/Documents/research/GreatSPN/DSPN-Tool-Release -load /home/edisone/Documents/research/GreatSPN/nets/MacroscopicTests/macroscopic.PNPRO.solution/GSPNC1 -epsilon 1.0E-7 -on-the-fly -i -i-power -rpar AR1 4.0 -rpar BR1 2.0 -mpar I 1 -mpar NR1 2 -rpar pr1 400.0 -rpar pr2 100.0 -rpar r 500.0 -s -all-measures'
args = shlex.split(cmdTransient)
#result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
#print(result.returncode, "\n", result.stdout, "\n", result.stderr)
#print(result.stdout)

pmax = 3								# number of points
iterations = pmax * 10					# number of iterations
t = np.linspace(0, pmax, iterations)	# time grid

X = np.zeros((len(t), S + 1)) #vector of populations

#'''
#----- STOCHASTIC TRANSIENT SIMULATION -----
args[17] = N 	#number of entities
args[20] = R	#number of resources

start_time = time.time()

for i in range(0, iterations - 1):
	args[31] = str(t[i]) # transient time t_i

	aux = subprocess.check_output(args)
	out = aux.splitlines()

	stop = False

	for line in range(0, len(out)):
		if stop == True:
			break
		if b"COMPUTING BASIC PETRI NET MEASURES." in out[line]:			
			j = 1
			while j < Nplaces:
				res = out[line + j].split(b"=")				
				X[i, j - 1] = float(res[len(res) - 1].strip())
				j = j + 1
			stop = True

strtransient = "--- {} seconds (TRANSIENT - {} iterations) ---\n".format(time.time() - start_time, iterations)
file.write(strtransient)
print(strtransient)


#----- STOCHASTIC STEADY SIMULATION -----
args = shlex.split(cmdSteady)
args[17] = N
args[20] = R	#number of resources

start_time = time.time()
aux = subprocess.check_output(args)

strsteady = "--- {} seconds (STEADY) ---\n".format(time.time() - start_time)
file.write(strsteady)
print(strsteady)

out = aux.splitlines()
stop = False
for line in range(0, len(out)):
	if stop:
		break;
	if b"COMPUTING BASIC PETRI NET MEASURES." in out[line]:			
		j = 1
		while j < Nplaces:
			res = out[line + j].split(b"=")
			file.write("{}\n".format(out[line + j]))
			X[iterations - 1, j - 1] = float(res[len(res) - 1].strip())			
			j = j + 1
		stop = True

#----- PLOT SIMULATION -----
import matplotlib.pyplot as plt
plt.plot(t, X[:, 0], 'gs:',
	 t, X[:, 3], 'k*-',	 	 
	 t, X[:, 1], 'g.-',
     t, X[:, 4], 'bs',
     t, X[:, 5], 'rs',
     t, X[:, 2], 'r--')
plt.xlabel('tempo')
plt.ylabel('fichas')
plt.legend(['P0', 'P1', 'P2', 'P3', 'P4', 'R1'])
plt.savefig('microscopic-I' + N + '-R' + R + '.pdf', bbox_inches='tight')
#show()
#'''

# SIMULATION OF STEADY STATES FOR VARIOUS 'N'

'''
args = shlex.split(cmdSteady)

for k in range(1, int(N)):

	args[20] = str(k)
	start_time = time.time()
	aux = subprocess.check_output(args)

	strsteady = "--- {} seconds (STEADY) ---\n".format(time.time() - start_time)
	file.write(strsteady)
	#print(strsteady)

	out = aux.splitlines()
	stop = False
	for line in range(0, len(out)):
		if stop:
			break;
		if b"COMPUTING BASIC PETRI NET MEASURES." in out[line]:			
			j = 1
			while j < Nplaces:
				res = out[line + j].split(b"=")
				file.write("{}\n".format(out[line + j]))
				X[iterations - 1, j - 1] = float(res[len(res) - 1].strip())
				#print(res)
				j = j + 1
			stop = True
			print(X[iterations - 1, 1] + X[iterations - 1, 5])
'''
