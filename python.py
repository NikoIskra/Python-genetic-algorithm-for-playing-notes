# Python3 program to create target string, starting from
# random string using Genetic Algorithm
import time
import musicalbeeps
import random

player = musicalbeeps.Player(volume = 1,
							mute_output = False)

#randomize=random.randrange(0,2)
randomize=0

MU=0.1

# Number of individuals in each generation
POPULATION_SIZE = 100

# Valid genes
GENES = '''ABCDEFG'''

MARY="EDCDEEEDDDEGG"

LONDON="GAGFEFGDEFEFGGAGFEFGDGEC"

JINGLE="EEEEEEEGCDEFFFFFEEEEDDEDGEEEEEEEGCDEFFFFFEEEGGFDCEEEEEE"



# Target string to be generated
TARGET = MARY

class Individual(object):
	'''
	Class representing individual in population
	'''
	def __init__(self, chromosome): 
		self.chromosome = chromosome
		self.fitness = self.cal_fitness()

	def __getitem__(self, item):
		return self.chromosome[item]

	@classmethod
	def mutated_genes(self):
		'''
		create random genes for mutation
		'''
		global GENES
		gene = random.choice(GENES)
		return gene

	@classmethod
	def create_gnome(self):
		'''
		create chromosome or string of genes
		'''
		global TARGET
		gnome_len = len(TARGET)
		return [self.mutated_genes() for _ in range(gnome_len)]

	def mate(self, par2):
		'''
		Perform mating and produce new offspring
		'''

		child_chromosome = []
		for gp1, gp2 in zip(self.chromosome, par2.chromosome):	

			prob = random.random()

			if prob < (1-MU)/2:
				child_chromosome.append(gp1)

			elif prob < 1-MU:
				child_chromosome.append(gp2)

			else:
				child_chromosome.append(self.mutated_genes())
		return Individual(child_chromosome)

	def cal_fitness(self):
		global TARGET
		fitness = 0
		for gs, gt in zip(self.chromosome, TARGET):
			if gs != gt: fitness+= 1
		return fitness

def main():
	start=time.time()
	global POPULATION_SIZE

	generation = 1

	found = False
	population = []

	for _ in range(POPULATION_SIZE):
				gnome = Individual.create_gnome()
				population.append(Individual(gnome))

	while not found:

		population = sorted(population, key = lambda x:x.fitness)

		if population[0].fitness <= 0:
			found = True
			end=time.time()
			print("vrijeme: " + str(round(end-start, 4)))
			kromosom=population[0]
			i=0
			if (randomize==0):
				for _ in range(len(kromosom.chromosome)):
					nota=kromosom.chromosome[i]
					player.play_note(nota, 0.2)
					i+=1
			else:
				for _ in range(len(kromosom.chromosome)):
					nota=kromosom.chromosome[i]
					oktava=random.randrange(4, 9)
					odabir=random.randrange(0,4)
					prob = random.random()
					if (odabir==0):
						player.play_note(nota, prob)
					elif(odabir==1):
						player.play_note(nota + str(oktava), prob)
					elif(odabir==2):
						sharp=random.randrange(0,2)
						if (sharp==0):
							x='#'
						elif(sharp==1):
							x='b'
						player.play_note(nota + x, prob)
					elif(odabir==3):
						sharp=random.randrange(0,2)
						if (sharp==0):
							x='#'
						elif(sharp==1):
							x='b'
						player.play_note(nota + str(oktava) + x, prob)
					else:
						player.play_note(nota, prob)
					i+=1
			break

		new_generation = []

		s = int((10*POPULATION_SIZE)/100)
		new_generation.extend(population[:s])

		s = int((90*POPULATION_SIZE)/100)
		for _ in range(s):
			parent1 = random.choice(population[:50])
			parent2 = random.choice(population[:50])
			child = parent1.mate(parent2)
			new_generation.append(child)

		population = new_generation

		print("Generation: {}\tString: {}\tFitness: {}".\
			format(generation,
			"".join(population[0].chromosome),
			population[0].fitness))

		generation += 1

	
	print("Generation: {}\tString: {}\tFitness: {}".\
		format(generation,
		"".join(population[0].chromosome),
		population[0].fitness))

if __name__ == '__main__':
	main()