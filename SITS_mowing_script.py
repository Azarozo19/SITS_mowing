import os
import glob
from SITS_mowing.utils.utils import mosaic_rasters
from utils.utils import create_folder_structure, execute_cmd
from utils.force_class_utils import force_class_udf

# define paths
base_path = '/rvt_mount'                                                               # Base Path where ./process/ folder structure should be created
project_name = "brandemburg"                                                         # Project Name defined for vitalitat_3cities_data storage
force_dir = "/force:/force"                                                             # Mount Point for Force-Datacube
local_dir = f"{base_path}:{base_path}"                                                  # Mount Point for local Drive
hold = False                                                                              #if True, cmd must be closed manually - recommended for debugging FORCE

# define parameters
date_range = "2023-01-01 2023-12-30"                                                      # format YYYY-MM-DD YYYY-MM-DD
aois = glob.glob("/rvt_mount/mowing_detection/process/data/BB_25833_3035.shp") # Define multiple or single AOI-Shapefile


#Functions
create_folder_structure(base_path)                                                      #create folder structure
force_class_udf(project_name, force_dir, local_dir, base_path, aois, hold, date_range) # Creates the parameter and the UDF file
basename = os.path.basename (aois[0])                                                   #aois directory path
execute_cmd(hold, local_dir, force_dir,base_path, project_name, basename)               # Runs FORCE function
mosaic_rasters(base_path, project_name, basename, aoi_path=aois[0], dtype="int16")      #Merge and clip the output tiles


