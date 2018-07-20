# force floating point division. Can still use integer with //
from __future__ import division
# other good compatibility recquirements for python3
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
# This file is used for importing the common utilities classes.
import numpy as np
import matplotlib.pyplot as plt
import sys, re
sys.path.append("../")
from Code import _command_line_config,Detector, UtilFEATHER, Analysis
from UtilForce.FEC import FEC_Util


def _get_file_info(in_file):
    """
    :param in_file: file to read, formatted as FEATHER requires
    :return:
    """
    data = np.loadtxt(in_file,delimiter=',',skiprows=0)
    header_info = _command_line_config._parse_csv_header(in_file)
    time,sep,force = data[:,0],data[:,1],data[:,2]
    file_dict = dict(spring_constant=header_info.spring_constant,
                     trigger_time = header_info.trigger_time,
                     dwell_time = header_info.dwell_time)
    return time,sep,force, file_dict

def _plot_results(time,force,event_indices_1):
    """
    :param time: in seconds
    :param force:  in N
    :param event_indices_1: indices into force where we predict an event
    :return: nothing, shows a plot
    """
    force_pN = force*-1e12
    force_pN_zero = force_pN - force_pN[force_pN.size//10]
    plt.plot(time,force_pN_zero)
    for i in event_indices_1:
        plt.axvline(time[i],color='r',linestyle='--')
    plt.xlabel("Time (s)")
    plt.ylabel("Force (pN)")
    plt.show()

def _test_FEATHER_retract_only(fec,threshold,tau):
    """
    :param fec: the force-extension curve, from (e.g.)
    _command_line_config.make_fec

    :param threshold: the significance threshold
    :param tau: the fractional smoothing
    :return:
    """
    # # Next, we show how to get do event detection based only on the approach
    # We do the following steps(1-4), below
    #       (1) Create a new FEC based only on the retract
    # first, we get just the retract, which starts at t=(TriggerTime+DwellTime)
    retract = Analysis.zero_and_split_force_extension_curve(fec,tau).retract
    # next, we use <pct_pseudo_approach> of the retract to make an approach
    pct_pseudo_approach = 0.1
    split = UtilFEATHER._split_from_retract(retract,pct_pseudo_approach,tau)
    # combined the 'fake' approach and retract
    to_save = FEC_Util._create_psuedo_fec_to_save(split)
    to_save.Meta.SourceFile = "TemporaryFEC"
    #       (2) Save the FEC out to a csv
    file_saved = FEC_Util._save_single_csv(out_dir="./", fec_to_save=to_save)
    #       (3) Run FEATHER on the CSV, just as we did above
    time, sep, force, file_dict = _get_file_info(file_saved)
    meta_dict = dict(threshold=threshold,tau=tau,**file_dict)
    event_indices_1 = _command_line_config.run_feather(in_file=file_saved,
                                                       **meta_dict)
    _plot_results(time,force,event_indices_1)

def _analyze_file(in_file):
    threshold = 1e-3
    tau = 2e-2
    time, sep, force, file_dict = _get_file_info(in_file)
    meta_dict = dict(threshold=threshold,tau=tau,**file_dict)
    event_indices_1 = _command_line_config.run_feather(in_file=in_file,
                                                       **meta_dict)
    # # (2) directly, using python arrays and a constructed fec object. This is
    # #    likely to be much faster, since there is no extra file IO.
    fec = _command_line_config.make_fec(time=time,separation=sep,force=force,
                                        **meta_dict)
    event_indices_2 = _command_line_config.predict_indices(fec,
                                                           tau_fraction=tau,
                                                           threshold=threshold)
    # make sure the two methods are consistent
    assert np.allclose(event_indices_1,event_indices_2) , \
        "Programming error; FEATHER methods should be identical"
    # POST: they are consistent. go ahead and plot force vs time, add lines
    # where an event is predicted
    print("Found events at indices: {}".format(event_indices_1))
    # # Next, we show how to get do event detection based only on the approach
    # We do the following steps(1-4), below
    #       (1) Create a new FEC based only on the retract
    #       (2) Save the FEC out to a csv
    #       (3) Run FEATHER on the CSV, just as we did above
    _test_FEATHER_retract_only(fec,threshold,tau)

    
    

def run():
    """
    <Description>

    Args:
        param1: This is the first param.
    
    Returns:
        This is a description of what is returned.
    """
    # there are a couple of ways to call FEATHER in python. 
    # # (1) through an intermediate '.csv' file
    for i in range(19):
        in_file = '../Data/example_{:d}.csv'.format(i)
        _analyze_file(in_file)
    

if __name__ == "__main__":
    run()
