# In The Name Of God


from Modules.mission_analysis.mission_module import mission_analyzer
from Modules.dv_analysis.dv_module import mission_function_extractor

from Helpers.utility import print_dict_items

# 1. Analyzing mission
mission_type = input('Please Enter Mission Type (LEO/GEO):')
if mission_type == 'GEO':
    print('Undefined Mission. Exiting...')
    exit()

mission_functions = mission_analyzer(mission_type)
print('========== Mission Funtions ==========')
print_dict_items(mission_functions)

dv_total, m_attitude_control_percent = mission_function_extractor(mission_functions)
print('========== Mission Design Outputs ==========')
print(f'Total Required dv: {dv_total} m/s')
print(f'attitude control mass percentage: {m_attitude_control_percent} ({m_attitude_control_percent*100}%)')