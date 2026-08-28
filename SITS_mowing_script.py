<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from pathlib import Path
import cProfile
import pstats
import time

from utils.force_class_utils import force_class_udf
from utils.utils import create_folder_structure, execute_cmd, export_selected_mowing_bands


BASE_PATH = Path("/rvt_mount")
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
PROJECT_NAME = "mowing_2021_germany_1tile_"
=======
PROJECT_NAME = "mowing_2018_germany"
>>>>>>> 24c0c30 (second commit)
FORCE_DIR = "/force:/force"
LOCAL_DIR = f"{BASE_PATH}:{BASE_PATH}"
HOLD = False
CLEAN_RERUN = True
ENABLE_PROFILING = False
PROFILE_OUTPUT = "sits_mowing_profile.prof"

DATE_RANGE = "2018-01-01 2018-12-31"
AOIS = sorted(BASE_PATH.glob("3DTests/data/harm_data/shp_germany_border.shp"))


def process_aoi(aoi_path):
    basename = aoi_path.name

    force_class_udf(
        project_name=PROJECT_NAME,
        force_dir=FORCE_DIR,
        local_dir=LOCAL_DIR,
        base_path=str(BASE_PATH),
        aois=[str(aoi_path)],
        hold=HOLD,
        date_range=DATE_RANGE,
        clean=CLEAN_RERUN,
    )
    execute_cmd(HOLD, LOCAL_DIR, FORCE_DIR, str(BASE_PATH), PROJECT_NAME, basename)

    output_path = export_selected_mowing_bands(
        base_path=str(BASE_PATH),
        project_name=PROJECT_NAME,
        basename=basename,
        aoi_path=str(aoi_path),
    )
    print(f"Finished AOI {basename}: {output_path}")


def main():
    if not AOIS:
        raise FileNotFoundError("No AOI shapefiles matched the configured AOI pattern.")

    create_folder_structure(str(BASE_PATH), PROJECT_NAME)

    for aoi_path in AOIS:
        process_aoi(aoi_path)


if __name__ == "__main__":
    if ENABLE_PROFILING:
        profiler = cProfile.Profile()
        start_time = time.time()

        profiler.enable()
        main()
        profiler.disable()

        total_time = time.time() - start_time
        print(f"Total execution time: {total_time:.2f}s")

        stats = pstats.Stats(profiler).sort_stats("cumtime")
        stats.print_stats(30)
        stats.dump_stats(PROFILE_OUTPUT)
        print(f"cProfile data written to {PROFILE_OUTPUT}")
    else:
        main()
=======
import subprocess
import time
=======
>>>>>>> 00bcb7d (Mosaic step)
import os
import glob
from SITS_mowing.utils.utils import mosaic_rasters
from utils.utils import create_folder_structure, execute_cmd
=======
from pathlib import Path

>>>>>>> 8739a86 (merge and number of bands fixed)
from utils.force_class_utils import force_class_udf
from utils.utils import create_folder_structure, execute_cmd, export_selected_mowing_bands


<<<<<<< HEAD
#Functions
create_folder_structure(base_path)                                                      #create folder structure
force_class_udf(project_name, force_dir, local_dir, base_path, aois, hold, date_range) # Creates the parameter and the UDF file
basename = os.path.basename (aois[0])                                                   #aois directory path
execute_cmd(hold, local_dir, force_dir,base_path, project_name, basename)               # Runs FORCE function
<<<<<<< HEAD
<<<<<<< HEAD

>>>>>>> 89c9170 (version 0.1)
=======
>>>>>>> 26d907e (version 0.1)
=======
mosaic_rasters(base_path, project_name, basename, aoi_path=aois[0], dtype="int16")      #Merge and clip the output tiles


>>>>>>> 00bcb7d (Mosaic step)
=======
BASE_PATH = Path("/rvt_mount")
PROJECT_NAME = "germany"
=======
PROJECT_NAME = ""
>>>>>>> 80e689e (Optimize mowing UDF and add local benchmark workflow)
=======
PROJECT_NAME = "mowing_2018_germany"
>>>>>>> c2ec45f (Readme fixed)
=======
PROJECT_NAME = "mowing_2021_germany_1tile_"
>>>>>>> 2542a81 (Update mowing runtime configuration and UDF safeguards)
FORCE_DIR = "/force:/force"
LOCAL_DIR = f"{BASE_PATH}:{BASE_PATH}"
HOLD = False
CLEAN_RERUN = True
RUN_FORCE = True
ENABLE_PROFILING = True
PROFILE_OUTPUT = "sits_mowing_profile.prof"

DATE_RANGE = "2021-01-01 2021-12-31"
AOIS = sorted(BASE_PATH.glob("3DTests/data/xml/1_2021_2024_v1_0.shp"))


def process_aoi(aoi_path):
    basename = aoi_path.name

    if RUN_FORCE:
        force_class_udf(
            project_name=PROJECT_NAME,
            force_dir=FORCE_DIR,
            local_dir=LOCAL_DIR,
            base_path=str(BASE_PATH),
            aois=[str(aoi_path)],
            hold=HOLD,
            date_range=DATE_RANGE,
            clean=CLEAN_RERUN,
        )
        execute_cmd(HOLD, LOCAL_DIR, FORCE_DIR, str(BASE_PATH), PROJECT_NAME, basename)

    output_path = export_selected_mowing_bands(
        base_path=str(BASE_PATH),
        project_name=PROJECT_NAME,
        basename=basename,
        aoi_path=str(aoi_path),
    )
    print(f"Finished AOI {basename}: {output_path}")


def main():
    if not AOIS:
        raise FileNotFoundError("No AOI shapefiles matched the configured AOI pattern.")

    create_folder_structure(str(BASE_PATH), PROJECT_NAME)

    for aoi_path in AOIS:
        process_aoi(aoi_path)


if __name__ == "__main__":
    if ENABLE_PROFILING:
        profiler = cProfile.Profile()
        start_time = time.time()

<<<<<<< HEAD
    profiler.enable()
    main()
<<<<<<< HEAD
>>>>>>> 8739a86 (merge and number of bands fixed)
=======
    profiler.disable()
=======
        profiler.enable()
        main()
        profiler.disable()
>>>>>>> c2ec45f (Readme fixed)

        total_time = time.time() - start_time
        print(f"Total execution time: {total_time:.2f}s")

<<<<<<< HEAD
    stats = pstats.Stats(profiler).sort_stats("cumtime")
    stats.print_stats(30)
    stats.dump_stats(PROFILE_OUTPUT)
    print(f"cProfile data written to {PROFILE_OUTPUT}")
>>>>>>> 80e689e (Optimize mowing UDF and add local benchmark workflow)
=======
        stats = pstats.Stats(profiler).sort_stats("cumtime")
        stats.print_stats(30)
        stats.dump_stats(PROFILE_OUTPUT)
        print(f"cProfile data written to {PROFILE_OUTPUT}")
    else:
        main()
>>>>>>> c2ec45f (Readme fixed)
