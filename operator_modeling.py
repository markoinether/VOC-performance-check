import random


class MyClass:
    def __init__(self, id, total_elements):
        self.id = id
        self.elements = {i + id * total_elements for i in range(total_elements)}
        self.selected_elements = set()

    def add_element(self, element):
        if element in self.elements:
            self.selected_elements.add(element)

    @property
    def is_complete(self):
        return len(self.selected_elements) >= 5


def monte_carlo_simulation(n):
    total_elements = 7
    instances = [MyClass(i, total_elements) for i in range(n)]
    all_elements = range(1, total_elements * n + 1)

    for _ in range(int(0.3 * total_elements * n)):
        chosen_element = random.choice(all_elements)
        for instance in instances:
            instance.add_element(chosen_element)

    complete_instances = sum(1 for instance in instances if instance.is_complete)
    return complete_instances


# Example usage
n = 10  # Number of instances
result = monte_carlo_simulation(n)
print(f"Number of 'complete' instances: {result}")
