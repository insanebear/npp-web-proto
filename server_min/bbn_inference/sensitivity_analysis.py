import pymc as pm
import numpy as np
from scipy import stats
from .bbn_utils import run_sampling, from_posterior

def filter_outsiders(data, threshold=3):
    z_scores = stats.zscore(data[0])
    mask = np.abs(z_scores) < threshold
    return data[0][mask]

def demand_model_func(demand, observed_failures, pfd_trace):
    demand_model = pm.Model()
    with demand_model:
        pfd_prior = from_posterior("pfd_prior", pfd_trace, bins=1000)
        failures = pm.Binomial("failures", n=demand, p=pfd_prior, observed=observed_failures)
    return demand_model

def get_confidence(data, goal):
    return np.count_nonzero(data <= goal) / data["draw"].size

max_demand = 25000
demand_interval = 1000
demand_start = 1000
max_trial = 10 # used to prevent infinite loop

def get_number_of_required_demand(trace, pfd_goal, confidence_goal):
    # filter out outliers for interpolation
    filtered_pfd_trace = filter_outsiders(trace.posterior["PFD"])

    # confidence level of pfd trace obtained from BBN model
    original_confidence = get_confidence(trace.posterior["PFD"], pfd_goal)

    demand_traces = [] # used for debugging
    demands = []
    max_confidence = original_confidence
    confidence_levels = []
    means = []

    demand = demand_start
    print("Sensitivity Analysis start!")
    while demand <= max_demand:
        print("number of demands: ", demand)
        demands.append(demand)
        confidence = 0
        trial = 0
        while confidence < max_confidence:
            demand_trace = run_sampling(model=demand_model_func(demand=demand, observed_failures=0, pfd_trace=filtered_pfd_trace))
            confidence = get_confidence(demand_trace.posterior["pfd_prior"], pfd_goal)
            print("confidence: ", confidence)
            max_confidence = max(confidence, max_confidence)
            trial += 1
            if trial == max_trial:
                break
        confidence_levels.append(confidence)
        means.append(demand_trace.posterior["pfd_prior"].mean().item())
        demand_traces.append(demand_trace)
        if confidence == confidence_goal:
            return demand
        if confidence > confidence_goal:
            break
        demand += demand_interval
    print("Sensitivity Analysis finished!")

    # require calculation of number of demands
    for index, level in enumerate(confidence_levels):
        if level > confidence_goal and index == 0:
            return demand_start
        if level > confidence_goal and index >= 1:
            return ((confidence_goal - confidence_levels[index-1]) / (level - confidence_levels[index-1]) * demand_interval) + demands[index-1]

    return max_demand