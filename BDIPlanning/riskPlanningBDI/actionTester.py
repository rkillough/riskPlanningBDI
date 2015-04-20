import random

#takes a mean and a standard deviation and output the total reward after 1000 random numbers from a normal dist
def reward(mu, sigma):
    total = 0
    for i in range(1000):
        total += random.gauss(mu, sigma)
    return total
