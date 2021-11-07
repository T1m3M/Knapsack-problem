from random import choices, randint, randrange, random


class Knapsack:
    def __init__(self, size):
        self.size = size


class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value
        self.selected = False

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False


class Case:
    def __init__(self, numOfItems, maxKnapsackSize):
        self.numOfItems = numOfItems
        self.knapsack = Knapsack(maxKnapsackSize)
        self.items = []

    def add_item(self, weight, value):
        self.items.append(Item(weight, value))


def cases_preprocessing(file_data, total_cases):
    start = 0
    end = file_data.index('')
    case_num = 1
    cases_data = []

    # split cases data
    while case_num <= total_cases:
        cases_data.append(file_data[start:end])

        try:
            start = end + 2
            end = start + file_data[start:].index('')
        except ValueError:
            break

    return cases_data


def cases_parsing(cases_data):
    cases = []

    # parsing each case to an object
    for case_data in cases_data:
        total_items = int(case_data[0])
        size_of_knapsack = int(case_data[1])

        case = Case(total_items, size_of_knapsack)

        for item in case_data[2:]:
            item_data = [int(x) for x in item.split()]
            case.add_item(item_data[0], item_data[1])

        cases.append(case)

    return cases


def loading_test_cases():
    # reading test cases
    with open("input_example.txt") as f:
        file_lines = f.read().splitlines()

    total_cases = int(file_lines[0])

    # refine cases' data
    cases_data = cases_preprocessing(file_lines[2:], total_cases)

    # parsing cases in array of objects
    return cases_parsing(cases_data)


def genome_generation(genome_length):
    return choices([0, 1], k=genome_length)


def population_generation(population_size, genome_length):
    return [genome_generation(genome_length) for _ in range(population_size)]


def fitness(genome, items, weight_limit):
    value = 0
    weight = 0

    # calculating score of genome if feasible
    for i in range(len(genome)):
        if genome[i] == 1:
            weight += items[i].weight
            value += items[i].value

        if weight > weight_limit:
            return 0

    return value


def selection_pair(population, items, weight_limit):
    # selecting 2 pairs from population
    return choices(
        population=population,
        weights=[fitness(genome, items, weight_limit) for genome in population],
        k=2
    )


def crossover(genome_a, genome_b):
    # swapping chunks of bits at a random position
    random_position = randint(1, len(genome_a) - 1)
    return genome_a[0:random_position] + genome_b[random_position:], \
           genome_b[0:random_position] + genome_a[random_position:]


def mutation(genome, probability=0.5):
    # flipping a bit at random position
    random_position = randrange(len(genome))
    if random() <= probability:
        genome[random_position] = abs(genome[random_position] - 1)

    return genome


def run_evolution(case, population_size=10, generation_limit=100):
    population = population_generation(population_size, case.numOfItems)

    for generation_num in range(generation_limit):

        # sorting the population from best to worst according to fitness score
        population = sorted(
            population,
            key=lambda genome: fitness(genome, case.items, case.knapsack.size),
            reverse=True
        )

        # applying elitism approach (best 2 solutions remains in next generation)
        next_generation = population[:2]

        # picking random pairs and applying mutations (if possible)
        for j in range(int(len(population) / 2) - 1):
            parents = selection_pair(population, case.items, case.knapsack.size)
            offspring_a, offspring_b = crossover(parents[0], parents[1])

            offspring_a = mutation(offspring_a)
            offspring_b = mutation(offspring_b)

            next_generation += [offspring_a, offspring_b]

        population = next_generation

    # sorting the population from best to worst according to fitness score
    population = sorted(
        population,
        key=lambda genome: fitness(genome, case.items, case.knapsack.size),
        reverse=True
    )

    # returning best solution and generation number
    return population[0], generation_num + 1


def decode_genome(items, genome):
    for i in range(len(genome)):
        if genome[i] == 1:
            print(f"{items[i].weight} {items[i].value}")


def main():
    # loading test cases in array of objects
    cases = loading_test_cases()

    # evolution of the algorithm
    solution, generation_num = run_evolution(cases[0])

    total_weight = fitness(solution, cases[0].items, cases[0].knapsack.size)

    print(f"Case #0: {total_weight}")
    
    # number of items that fit in knapsack
    print(solution.count(1))

    # decode genome to items
    decode_genome(cases[0].items, solution)


if __name__ == '__main__':
    main()
