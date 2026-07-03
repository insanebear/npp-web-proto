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
    return np.count_nonzero(data <= goal) / data.size

max_demand = 25000
demand_interval = 200
demand_start = 1
N_RUNS = 3  # number of independent MCMC runs averaged per grid point (replaces the re-sampling loop)

def get_number_of_required_demand(trace, pfd_goal, confidence_goal, draws, tune, chains, thin):
    # filter out outliers for interpolation
    filtered_pfd_trace = filter_outsiders(trace.posterior["PFD"])

    demand_traces = [] # used for debugging
    demands = []
    confidence_levels = []
    means = []

    demand = demand_start
    print("Sensitivity Analysis start!")
    while demand <= max_demand:
        print("number of demands: ", demand)
        demands.append(demand)

        # Estimate confidence at this grid point by averaging N_RUNS independent MCMC runs.
        # (Replaces the previous re-sampling loop that resampled until the confidence exceeded
        #  the running maximum, which biased the estimate toward the upper tail and caused the
        #  required demand to be under-estimated.)
        conf_samples = []
        for _ in range(N_RUNS):
            demand_model = demand_model_func(demand=demand, observed_failures=0, pfd_trace=filtered_pfd_trace)
            demand_trace = run_sampling(model=demand_model, draws=draws, tune=tune, chains=chains, thin=thin)
            conf_samples.append(get_confidence(demand_trace.posterior["pfd_prior"], pfd_goal))
        confidence = float(np.mean(conf_samples))
        print("confidence (mean of {} runs): {}".format(N_RUNS, confidence))

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
