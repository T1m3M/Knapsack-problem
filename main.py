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


def main():
    return


if __name__ == '__main__':
    main()
