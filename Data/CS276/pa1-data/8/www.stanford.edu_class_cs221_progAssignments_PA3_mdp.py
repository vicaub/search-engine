mdp py licensing information please do not distribute or publish solutions to this project you are free to use and extend these projects for educational purposes the pacman ai projects were developed at uc berkeley primarily by john denero denero cs berkeley edu and dan klein klein cs berkeley edu for more info see http inst eecs berkeley edu cs188 sp09 pacman html import random class markovdecisionprocess def getstates self return a list of all states in the mdp not generally possible for large mdps abstract def getstartstate self return the start state of the mdp abstract def getpossibleactions self state return list of possible actions from state abstract def gettransitionstatesandprobs self state action returns list of nextstate prob pairs representing the states reachable from state by taking action along with their transition probabilities note that in q learning and reinforcment learning in general we do not know these probabilities nor do we directly model them abstract def getreward self state action nextstate get the reward for the state action nextstate transition not available in reinforcement learning abstract def isterminal self state returns true if the current state is a terminal state by convention a terminal state has zero future rewards sometimes the terminal state s may have no possible actions it is also common to think of the terminal state as having a self loop action pass with zero reward the formulations are equivalent abstract
