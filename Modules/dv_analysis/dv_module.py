# In The Name Of God


import random
from math import sqrt, pi

class Orbital_Maneuvers:
    def __init__(self, r_initial, r_final, *args, **kwargs):
        self.mu        = 3.986e5    # km^3/s
        self.r_initial = r_initial
        self.r_final   = r_final
    def hohmann_transfer(self):
        # Ref: Vallado, 4th ed, Algorithm 36:Hohmann Transfer
        # (r_initial, r_final)→ a_trans, τ_trans, Δv
        
        mu = self.mu
        r_final = self.r_final
        r_initial = self.r_initial
        
        a_trans   = (r_initial + r_final)/2
        v_initial = sqrt(mu/r_initial)
        v_trans_a = sqrt(2*mu/r_initial - mu/a_trans)
        v_final   = sqrt(mu/r_final)
        v_trans_b = sqrt(2*mu/r_final - mu/a_trans)
        dv_a      = v_trans_a - v_initial
        dv_b      = v_final - v_trans_b
        
        dv        = abs(dv_a) + abs(dv_b)
        tau_trans = pi * sqrt((a_trans**3)/self.mu)
        
        return a_trans, tau_trans, dv
    
    def Numerical_transfer(self, Thrust, m_sat):
        pass

def orbit_insertion_dv():
    dv = random.randint(1800, 2400) # m/s
    return dv

def station_keeping_dv():
    dv = random.randint(15, 75) # m/s
    return dv

def maneuver_dv(maneuver):
    # 'maneuver': Object: tuple=(false, r_i) or tuple=(low_thrust/high_thrust, r_i, r_f)
    maneuver_type = maneuver[0]
    r_i = maneuver[1]
    r_f = maneuver[2]
    
    orbit_maneuver = Orbital_Maneuvers(r_initial=r_i, r_final=r_f)
    
    if maneuver_type == 'high_thrust':
        a_trans, tau_trans, dv = orbit_maneuver.hohmann_transfer()
    elif maneuver_type == 'low_thrust':
        raise Exception("low_thrust maneuvers are not allowed yet!")
    return dv

def deorbit_dv():
    dv = random.randint(120, 150) # m/s
    return dv

def attitude_control_m():
    mass_percentage = random.randint(3, 10)/100 # percent
    return mass_percentage

def mission_function_extractor(mission_functions: dict) -> None:
    """
    This function is used to extract and identify type of
    missions that needs to be done.
    so the required dv according to it will be calculated.
    
    Inputs:
        mission_functions (dict or json): its keys are:
            'orbit_insertion': Bool (false)
            'station_keeping': Bool (true)
            'maneuver': Object: tuple=(false, r_i) or tuple=(low_thrust/high_thrust, r_i, r_f)
            'deorbit': Bool (true)
            'attitude_control': Bool (true)
    
    Outputs:
        dv_total: float
    """
    dv_orbit_insertion = 0
    dv_station_keeping = 0
    dv_maneuver = 0
    dv_deorbit = 0
    m_attitude_control_percent = 0
    
    if mission_functions['orbit_insertion']:
        dv_orbit_insertion = orbit_insertion_dv()
    
    if mission_functions['station_keeping']:
        dv_station_keeping = station_keeping_dv()
    
    if mission_functions['maneuver'][0] != False:
        dv_maneuver = maneuver_dv(mission_functions['maneuver'])
    
    if mission_functions['deorbit']:
        dv_deorbit = deorbit_dv()
    
    if mission_functions['attitude_control']:
        m_attitude_control_percent = attitude_control_m()
    
    dv_total = dv_orbit_insertion + dv_station_keeping + dv_maneuver + dv_deorbit
    return dv_total, m_attitude_control_percent
