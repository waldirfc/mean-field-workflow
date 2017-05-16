# mean field model for performance analysis of numerous instances workflow

Here is the scripts used to generate stochastic and deterministic trajectories for a workflow process in BPMN.

For each workflow there is a folder with an arbitary name for the workflow, inside is the model described by {_model_}-BPMN.eps file, also there are two main folders, named _"Microscopic"_ and _"ODE"_ wich contains the stochastic and deterministics solution respectively for the used model. Inside each of them there are various plotted figures obtained for different number of instances and unities of resource, also there is the python script used to generate that solutions.

An example of a solution figure can be the file _{microscopic-I1-R2}_.pdf, which means that that solution correspondes to a stochastic (microscopic) modeling with 1 instance and 2 unities of resource.
