import math
import random

def createChromosome(N):
	gen = [random.randint(0,9) for x in range(1,N+1)]
	return gen

def createPopulation(maxGen,N):
	population = []
	for i in range(1,N+1):
		population.append(createChromosome(maxGen))
	return population

def decodeChromosome(rb,ra,gen,min,max):
	pembilang = (ra-rb)
	penyebut1 = 0
	penyebut2 = 0
	cek =[0.1,0.01,0.001,0.0001,0.00001,0.000001,0.0000001,0.00000001,0.1,0.01,0.001,0.0001,0.00001,0.000001,0.0000001,0.00000001]
	for i in range(1,9):
		penyebut1 += 9*(pow(10,-i))
	for i in range(min,max):
		penyebut2 += gen[i]*cek[i]
	return(round(rb+((pembilang*penyebut2)/penyebut1),2))

def getFitness(x1,x2):
	h = (((4-2.1*1*(pow(x1,2)))+(pow(x1,4))/3)*pow(x1,2))+x1*x2+(((-4)+4*pow(x2,2)))*pow(x2,2)
	return 1/(h+1.5)

def cekNilai(x1,x2):
	return (((4-2.1*1*(pow(x1,2)))+(pow(x1,4))/3)*pow(x1,2))+x1*x2+(((-4)+4*pow(x2,2)))*pow(x2,2)

def bestFitness(population):
	max = 0
	idx = -1
	for i in population:
		x1 = decodeChromosome(-3,3,i,0,8)
		x2 = decodeChromosome(-2,2,i,8,16)
		cek = getFitness(x1,x2)
		if cek>max:
			max = cek
			idx = i
	return max,idx

def rouletteWheels(population):
	sumFitness = 0
	tmp =0
	countFitness = 0
	for i in population:		
		x1 = decodeChromosome(-3,3,i,0,8)
		x2 = decodeChromosome(-2,2,i,8,16)	
		sumFitness += getFitness(x1,x2)
	
	randomNumber = random.random()

	for i in population:
		x1 = decodeChromosome(-3,3,i,0,8)
		x2 = decodeChromosome(-2,2,i,8,16)
		countFitness += getFitness(x1,x2)
		if countFitness/sumFitness > randomNumber:
			return i
			break

def mate(parent1,parent2):
	cp = random.randint(1,8)
	child1 = []
	child2 = []
	for i in range(0,cp):
		child1.append(parent1[i])
		child2.append(parent2[i])
	for i in range(cp,16):
		child1.append(parent2[i])
		child2.append(parent1[i])

	child = [child1,child2]
	return child

def mutate(child):
	for i in range(0,len(child)):
		prob = random.random()
		if prob<0.5:
			child[i] = random.randint(0,9)
	return child

def elitism(population):
	bestLokal = []
	bestLokal = bestFitness(population)
	return bestLokal


#WORK 
population,child= [],[]
population = createPopulation(16,10)
generasi = 1
variansiFitnes = 0
stagnantCek = [True,0,0]
while (generasi <= 10000) and (stagnantCek[0]):
	newPop = []
	for i in range(0,4):
		parent1 = rouletteWheels(population)
		parent2 = rouletteWheels(population)
		child = mate(parent1,parent2)
		for gen in child:
			gen = mutate(gen)
			newPop.append(gen)
	
	bestLokal = elitism(population)
	newPop.append(bestLokal[1])
	population = newPop

	if stagnantCek[1] == bestLokal[0]:
		stagnantCek[2]+=1
		if stagnantCek[2] >= 500:
			stagnantCek[0] = False
	else:
		stagnantCek[1] = bestLokal[0]
		stagnantCek[2] = 0
		variansiFitnes += 1

	generasi+=1


x1 = decodeChromosome(-3,3,bestLokal[1],0,8)
x2 = decodeChromosome(-2,2,bestLokal[1],8,16)
print("Nilai Terkecil : ",cekNilai(x1,x2))
print("Fenotype :",x1,x2)
print("Gen :",bestLokal[1])
print("Fitness :,",bestLokal[0])
print("Variansi Fitness :",variansiFitnes)
print("Total Generasi :",generasi)
