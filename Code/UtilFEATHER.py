# force floating point division. Can still use integer with //
from __future__ import division
# This file is used for importing the common utilities classes.
import numpy as np
import matplotlib.pyplot as plt
import sys,warnings,copy
from scipy import interpolate
from scipy.stats import norm
from scipy.ndimage.filters import uniform_filter1d,generic_filter1d
from scipy.integrate import cumtrapz
from . import Detector, Analysis
from ..UtilForce.FEC.FEC_Util import TimeSepForceObj

def _manual_split(approach,dwell,retract,tau_n_points,
                  short_circuit_adhesion=False):
    """
    :param approach: to use for the no-event model
    :param dwell: if needed, can manually specify a dwell
    :param retract: actual data to use.
    :param tau_n_points: number of points for tau
    :param short_circuit_adhesion: if True, then the approach is just
    representative, and FEATHER wont attempt to find the surface by the
    method of the zero force crossing the baseline. Useful if the approach
    doesnt have an existing INVOLS portion
    :return:
    """
    # make a 'custom' split fec (this is what FEATHER needs for its noise stuff)
    split_fec = Analysis.split_force_extension(approach, dwell, retract,
                                               tau_n_points)
    # set the 'approach' number of points for filtering to the retract.
    split_fec.set_tau_num_points_approach(split_fec.tau_num_points)
    # set the predicted retract surface index to a few tau. This avoids looking
    #  at adhesion
    if short_circuit_adhesion:
        N = tau_n_points
        split_fec.get_predicted_retract_surface_index = lambda: N
        split_fec.get_predicted_approach_surface_index = \
            lambda : approach.Force.size
    return split_fec

def _split_from_retract(d,pct_approach,tau_f,**kw):
    """
    :param d: retract-only curve
    :param pct_approach: how much of the *end* of the retract to use for the
    'effective' approach. Shouldn't have any events
    :param tau_f: fraction to use for tau
    :return: split_fec object
    """
    force_N = d.Force
    # use the last x% as a fake 'approach' (just for noise)
    n = force_N.size
    n_approach = int(np.ceil(n * pct_approach))
    tau_n_points = int(np.ceil(n * tau_f))
    # slice the data for the approach, as described above
    n_approach_start = n - (n_approach + 1)
    retract = d._slice(slice(0,None,1))
    fake_approach = d._slice(slice(n_approach_start, n, 1))
    fake_dwell = d._slice(slice(n_approach_start - 1, n_approach_start, 1))
    split_fec = _manual_split(approach=fake_approach, dwell=fake_dwell,
                              retract=retract,tau_n_points=tau_n_points,
                              **kw)
    return split_fec

def _detect_retract_FEATHER(d,pct_approach,tau_f,threshold,f_refs=None):
    """
    :param d:  TimeSepForce
    :param pct_approach: how much of the retract, starting from the end,
    to use as an effective approach curve
    :param tau_f: fraction for tau
    :param threshold: FEATHERs probability threshold
    :return: tuple of <output of Detector._predict_split_fec, tau number of
    points>
    """
    split_fec =  _split_from_retract(d,pct_approach,tau_f,
                                     short_circuit_adhesion=True)
    tau_n_points = split_fec.tau_num_points
    pred_info = Detector._predict_split_fec(split_fec, threshold=threshold,
                                            f_refs=f_refs)
    return pred_info, tau_n_points


def _create_psuedo_fec_to_save(fec_w_stats):
    """
    :param fec_w_stats:  a force-extension curve, where the approach is
    assumed to be taken from the end of the retract 
    :return: a new force-extension curve, such that the approach is from 0 to
    TriggerTime, and the Retract is from TriggerTime to the end
    """
    approach = fec_w_stats.approach._slice(slice(0,None,1))
    retract = fec_w_stats.retract._slice(slice(0,None,1))
    # 'fix' the approach so the z makes sense
    offset_x = max(approach.Separation)
    approach.ZSnsr -= offset_x
    approach.Separation -= offset_x
    # add on the retract minimum
    offset_x_retract = min(retract.Separation)
    approach.ZSnsr += offset_x_retract
    approach.Separation += offset_x_retract
    # reset the time bases
    approach.Time -= min(approach.Time)
    # set the retract to start immediately ater
    retract_start_time = max(approach.Time)
    dt = retract.Time[1] - retract.Time[0]
    retract.Time -= (min(retract.Time) - retract_start_time)
    retract.Time += dt
    # combine all the waves
    cat = lambda f: np.concatenate( [f(approach),f(retract)])
    time = cat(lambda x_tmp: x_tmp.Time)
    sep = cat(lambda x_tmp: x_tmp.Separation)
    force = cat(lambda x_tmp: x_tmp.Force)
    z = cat(lambda x_tmp: x_tmp.ZSnsr)
    # make a new TimeSepForce object...
    dict_v = TimeSepForceObj._meta_dict(SpringConstant=approach.SpringConstant,
                                        Velocity=approach.Velocity,Invols=1,
                                        DwellSetting=0,DwellTime=0,
                                        Name="")
    dict_v['TriggerTime'] = min(retract.Time)
    to_ret = TimeSepForceObj._cols_to_TimeSepForceObj(time=time,sep=sep,
                                                      force=force,
                                                      meta_dict=dict_v)
    events = [ [e[0],e[1]] for e in retract.Events]
    to_ret.set_events(events)
    # set the FEC to be negative, since FEATHER flips it by default
    to_ret.Force *= -1
    return to_ret
