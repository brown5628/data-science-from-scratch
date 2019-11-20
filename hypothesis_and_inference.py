from typing import Tuple
import math

def normal_approximation_to_binomial(n: int, p: float) -> Tuple[float, float]:
    """Returns mu and sigma corresponding to a Binomial(n, p)"""
    mu = p * n
    sigma = math.sqrt(p * (1 - p) * n)
    return mu, sigma

#import os
#os.chdir("C:\\Users\\brown\\Desktop\\learning_projects\\data-science-from-scratch")
from probability import normal_cdf

# the normal cdf _is_ the probability the variable is below a threshold
normal_probability_below = normal_cdf

# It's above the threshould if it's not below the threshold
def normal_probability_above(lo: float,
                            mu: float = 0,
                            sigma: float = 1) -> float:
    """The probability that an N(mu, sigma) is greater than lo"""
    return 1 - normal_cdf(lo, mu, sigma)

# It's between if it's less than hi but not less than lo
def normal_probability_between(lo: float,
                                hi: float,
                                mu: float = 0,
                                sigma: float = 1) -> float:
    """The probability than an N(mu, sigma) is between lo and hi."""
    return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)

# It's outside if it's not between
def normal_probability_outside(lo: float,
                                hi: float,
                                mu: float = 0,
                                sigma: float = 1) -> float:
    """The probability that an N(mu, sigma) is not between lo and hi."""
    return 1 - normal_probability_between(lo, hi, mu, sigma)

from probability import inverse_normal_cdf

def normal_upper_bound(probability: float,
                        mu: float = 0,
                        sigma: float = 1) -> float:
    """Returns the z for which P(Z <= z) = probability"""
    return inverse_normal_cdf(probability, mu, sigma)

def normal_lower_bound(probability: float,
                        mu: float = 0,
                        sigma: float = 1) -> float:
    """Returns the z for which P(Z <= z) = probability"""
    return inverse_normal_cdf(1 - probability, mu, sigma)

def normal_two_sided_bounds(probability: float,
                            mu: float = 0,
                            sigma: float = 1) -> Tuple[float, float]:
    """
    Returns the symetric (about the mean) bounds that contain the specified
    probability
    """
    tail_probability = (1 - probability) / 2

    # upper bound should have tail_probability above it
    upper_bound = normal_lower_bound(tail_probability, mu, sigma)

    # lower bound should have tail_probability below it
    lower_bound = normal_upper_bound(tail_probability, mu, sigma)

    return lower_bound, upper_bound

mu_0, sigma_0 = normal_approximation_to_binomial(1000,.5)

lower_bound, upper_bound = normal_two_sided_bounds(.95, mu_0, sigma_0)

# 95% bounds based on assumption p is 0.5
lo, hi = normal_two_sided_bounds(0.95, mu_0, sigma_0)

# actual mu and sigma based on p = 0.55
mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)

# a type 2 error means we fail to reject the null hypothesis,
# which will happen when X is still in our original interval
type_2_probability = normal_probability_between(lo, hi, mu_1, sigma_1)
power = 1 - type_2_probability

hi = normal_upper_bound(.95, mu_0, sigma_0)
# is 526 (< 531, since we need more proability in the upper tail)

type_2_probability = normal_probability_below(hi, mu_1, sigma_1)
power = 1 - type_2_probability

# %% codecell
# p-values
def two_sided_p_value(x: float, mu: float = 0, sigma: float = 1) -> float:
    """
    How likely are we to see a value at least as extreme as x (in either
    direction) if our values are from an N(mu, sigma)?
    """
    if x >= mu:
        # x is greater than the mean, so the tail is everything greater than x
        return 2 * normal_probability_above(x, mu, sigma)
    else:
        # x is less than the mean, so the tail is everything less than x
        return 2 * normal_probability_below(x, mu, sigma)

two_sided_p_value(529.5, mu_0, sigma_0)

import random

extreme_value_count = 0
for _ in range(1000):
    num_heads = sum(1 if random.random() < .5 else 0
                    for _ in range(1000))
    if num_heads >= 530 or num_heads <= 470:
        extreme_value_count += 1

# p-value was .-62 => ~62 extreme values out of 1000
assert 59 < extreme_value_count < 65, f"{extreme_value_count}"

two_sided_p_value(531.5, mu_0, sigma_0)

upper_p_value = normal_probability_above
lower_p_value = normal_probability_below

upper_p_value(524.5, mu_0, sigma_0)

upper_p_value(526.5, mu_0, sigma_0)

# %% codecell
# Confidence Intervals

#math.sqrt(p * (1 - p) / 1000)

p_hat = 525 / 1000
mu = p_hat
sigma = math.sqrt(p_hat * (1 - p_hat) / 1000)

normal_two_sided_bounds(.95, mu, sigma)

p_hat = 540 / 1000
mu = p_hat
sigma = math.sqrt(p_hat * (1 - p_hat) / 1000)
normal_two_sided_bounds(.95, mu, sigma)

# %% codecell
# p-hacking

from typing import List

def run_experiment() -> List[bool]:
    """Flips a fair coin 1000 times, True = heads, False = tails"""
    return [random.random() < .5 for _ in range(1000)]

def reject_fairness(experiment: List[bool]) -> bool:
    """Using the 5% significance levels"""
    num_heads = len([flip for flip in experiment if flip])
    return num_heads < 469 or num_heads > 531

random.seed(0)
experiments = [run_experiment() for _ in range(1000)]
num_rejections = len([experiment
                        for experiment in experiments
                        if reject_fairness(experiment)])

assert num_rejections == 46

# %% codecell
# Example: Running an A/B Test
