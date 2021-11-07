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


def main():
    cases = loading_test_cases()


if __name__ == '__main__':
    main()
