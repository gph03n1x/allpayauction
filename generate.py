import random

def generate_values(k, V, n):
    values = []
    for i in range(n):
        value = []
        upper_limit = V//2
        lower_limit = V//4
        for j in range(k-1):
            value.append(random.randint(lower_limit, upper_limit))
            print(upper_limit, lower_limit)
            upper_limit = lower_limit
            lower_limit = lower_limit//2

        value.append(V-sum(value))
        values.append(value)
        print(sum(value))
    return values

def generate_halved_budgets(V, k):
    return [V/2**i for i in range(k)]

if __name__ == "__main__":
    print(generate_values(5,1000, 1))
    print(generate_halved_budgets(1000, 5))
