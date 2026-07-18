# In The Name Of God


import pandas as pd
import numpy as np
import random
import os

SAT_DATA_FILEDIR = '\\Modules\\mission_analysis\\'
SAT_DATA_FILENAME = 'sat_missions_raw.xlsx'

class Mission_Architecture_Design:
    def __init__(self, mission_type, r_i, r_f):
        self.mission_type = mission_type
        self.r_i = r_i
        self.r_f = r_f
        
    def ai_call(self):
        try:
            a = 1/0
        except:
            print('Connection with AI failed.\nUsing Human Made Default Mission:')
            return self.offline_call()
    def offline_call(self):
        mission_functions = {
                            'orbit_insertion': False,
                            'station_keeping': True,
                            'maneuver': ('high_thrust', self.r_i, self.r_f),
                            'deorbit': True,
                            'attitude_control': True
                        }
        return mission_functions

def data_selector(file_dir=SAT_DATA_FILEDIR, filename=SAT_DATA_FILENAME):
    HERE = os.path.dirname(os.path.abspath(__file__))
    xlsx_path = os.path.join(HERE, "sat_missions_raw.xlsx")
    
    data = pd.read_excel(xlsx_path, index_col=None)
    
    rps = data['r_p (km)'].values
    ras = data['r_a (km)'].values
    
    masses = data['mass (kg)'].values
    
    lst = [rps[n] for n, i in enumerate(list(rps)) if (abs(rps[n] - ras[n]) < 50)]
    lst = np.array(lst)
    
    r_i = random.choice(lst)
    r_f = r_i + random.randint(50, 100)
    
    m_sat = np.average(masses)
    
    return r_i, r_f, m_sat

def mission_analyzer(mission_type):
    r_i, r_f, *args = data_selector()
    
    mission_architecture = Mission_Architecture_Design(mission_type, r_i, r_f)
    
    mission_functions = mission_architecture.ai_call()
    return mission_functions