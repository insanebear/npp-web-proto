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

demand_interval = 200
demand_start = 1
N_RUNS = 3  # number of independent MCMC runs averaged per grid point (replaces the re-sampling loop)

def get_max_demand(pfd_goal, confidence_goal, failures=0):
    # Analytic bound on the total demands needed to reach confidence_goal with
    # `failures` observed failures under a zero-information Beta(1,1) prior
    # (chi-square few-failure bound; failures=0 reduces to ceil(-ln(1-c)/pfd_goal)).
    # Replaces the fixed 25000 cap, which truncated the answer for failures >= 1.
    return int(np.ceil(stats.chi2.ppf(confidence_goal, 2 * (failures + 1)) / (2 * pfd_goal)))

def get_number_of_required_demand(trace, pfd_goal, confidence_goal, draws, tune, chains, thin,
                                  failures=0, tests_performed=0):
    # Returns (required_total_demand, goal_already_achieved).
    # `failures` enters the Binomial likelihood as observed evidence; `tests_performed`
    # only moves the search start point — confidence is monotone in demand for fixed
    # failures, so grid points below the demands already executed cannot contain the
    # crossing (Littlewood & Wright 1997: only the totals (N, j) matter, not when
    # the failures occurred).

    # filter out outliers for interpolation
    filtered_pfd_trace = filter_outsiders(trace.posterior["PFD"])

    demand_traces = [] # used for debugging
    demands = []
    confidence_levels = []
    means = []

    # Binomial likelihood requires demand >= failures
    demand = max(demand_start, failures, tests_performed)
    # keep the start point inside the search range so extreme tests_performed
    # values still get one confidence evaluation
    max_demand = max(get_max_demand(pfd_goal, confidence_goal, failures), demand)

    print("Sensitivity Analysis start! (failures={}, tests_performed={}, max_demand={})".format(
        failures, tests_performed, max_demand))
    while demand <= max_demand:
        print("number of demands: ", demand)
        demands.append(demand)

        # Estimate confidence at this grid point by averaging N_RUNS independent MCMC runs.
        # (Replaces the previous re-sampling loop that resampled until the confidence exceeded
        #  the running maximum, which biased the estimate toward the upper tail and caused the
        #  required demand to be under-estimated.)
        conf_samples = []
        for _ in range(N_RUNS):
            demand_model = demand_model_func(demand=demand, observed_failures=failures, pfd_trace=filtered_pfd_trace)
            demand_trace = run_sampling(model=demand_model, draws=draws, tune=tune, chains=chains, thin=thin)
            conf_samples.append(get_confidence(demand_trace.posterior["pfd_prior"], pfd_goal))
        confidence = float(np.mean(conf_samples))
        print("confidence (mean of {} runs): {}".format(N_RUNS, confidence))

        confidence_levels.append(confidence)
        means.append(demand_trace.posterior["pfd_prior"].mean().item())
        demand_traces.append(demand_trace)
        if confidence == confidence_goal:
            return demand, (len(demands) == 1 and tests_performed >= 1)
        if confidence > confidence_goal:
            break
        demand += demand_interval
    print("Sensitivity Analysis finished!")

    # require calculation of number of demands
    for index, level in enumerate(confidence_levels):
        if level > confidence_goal and index == 0:
            # goal already satisfied at the search start point; when demands were
            # already executed this means no further testing is needed
            return demands[0], tests_performed >= 1
        if level > confidence_goal and index >= 1:
            return ((confidence_goal - confidence_levels[index-1]) / (level - confidence_levels[index-1]) * demand_interval) + demands[index-1], False

    return max_demand, False
