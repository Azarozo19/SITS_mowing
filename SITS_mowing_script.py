import subprocess
import time
import os
import glob
from utils.utils import create_folder_structure, execute_cmd
from utils.force_class_utils import force_class_udf

# define paths
base_path = '/rvt_mount'                                                               # Base Path where ./process/ folder structure should be created
project_name = "git_test_dingo"                                                         # Project Name defined for vitalitat_3cities_data storage
force_dir = "/force:/force"                                                             # Mount Point for Force-Datacube
local_dir = "/rvt_mount:/rvt_mount"                                                        # Mount Point for local Drive
hold = True                                                                              #if True, cmd must be closed manually - recommended for debugging FORCE

# define parameters
date_range = "2023-01-01 2023-06-31"                                                      # format YYYY-MM-DD YYYY-MM-DD
aois = glob.glob("/rvt_mount/mowing_detection/process/data/Dingolfing_gmd_ex_3035.shp") # Define multiple or single AOI-Shapefile



create_folder_structure(base_path)                                                      #create folder structure
force_class_udf(project_name, force_dir, local_dir, base_path, aois, hold, date_range) # Creates the parameter and the UDF file
basename = os.path.basename (aois[0])                                                   #aois directory path
execute_cmd(hold, local_dir, force_dir,base_path, project_name, basename)               # Runs FORCE function
