from bbn_inference.bbn_utils import run_sampling
from bbn_inference.data import nrc_report_data
from bbn_inference.whole_model import create_whole_model

# this might take more than 30 minutes to run
def run_example_for_whole_model():
    data = nrc_report_data()
    model = create_whole_model(data)
    trace = run_sampling(model=model, numpyro=True, draws=1000, tune=1000)
    return trace
