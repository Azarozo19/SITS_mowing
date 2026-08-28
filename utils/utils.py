<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from __future__ import annotations
=======
>>>>>>> 24c0c30 (second commit)

import os
import glob
import subprocess
import time

import geopandas as gpd
import rasterio
from rasterio.merge import merge
from rasterio.io import MemoryFile
from rasterio.mask import mask
from tqdm import tqdm


def create_folder_structure(base_path, project_name):
    # Define the folder structure
    folder_structure = [
        'process',
        'process/data',
        'process/results',
        f'process/results/{project_name}',
        'process/temp',
        'process/temp/_mask'
    ]

<<<<<<< HEAD
=======
=======

>>>>>>> 8739a86 (merge and number of bands fixed)
=======
from __future__ import annotations

import json
>>>>>>> e1afd9e (Integrate tilewise mowing postprocessing)
import os
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from tqdm import tqdm


DEFAULT_BANDS = [1, 5, 6, 7, 8, 9, 10, 11]
REQUIRED_GDAL_TOOLS = ["gdalbuildvrt", "gdal_translate", "gdalwarp"]
DEFAULT_COMPRESSION = "DEFLATE"
DEFAULT_ZLEVEL = "9"
DEFAULT_BIGTIFF = "YES"
OUTPUT_NODATA = -9999
DEFAULT_BLOCKSIZE = 512
DEFAULT_OVERVIEW_LEVELS = [2, 4, 8, 16, 32, 64]
DEFAULT_OVERVIEW_RESAMPLING = "nearest"


@dataclass(frozen=True)
class TileCollection:
    tiles_root: Path
    tile_paths: list[Path]


def create_folder_structure(base_path, project_name):
    folder_structure = [
        "process",
        "process/data",
        "process/results",
        f"process/results/{project_name}",
        "process/temp",
        "process/temp/_mask",
    ]

<<<<<<< HEAD
    # Create each folder if it does not exist
>>>>>>> 89c9170 (version 0.1)
=======
>>>>>>> e1afd9e (Integrate tilewise mowing postprocessing)
=======
    # Create each folder if it does not exist
>>>>>>> 24c0c30 (second commit)
    for folder in folder_structure:
        path = os.path.join(base_path, folder)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created folder: {path}")
        else:
            print(f"Folder already exists: {path}")

<<<<<<< HEAD
<<<<<<< HEAD

def run_shell_command(cmd, hold=False):
    print(f"Running command:\n{cmd}\n")

    xterm_cmd = ['xterm']
    if hold:
<<<<<<< HEAD
        print("`hold=True` requested. Command output will stay in the current terminal.")
=======

def run_shell_command(cmd, hold=False):
    print(f"Running command:\n{cmd}\n")
    if hold:
<<<<<<< HEAD
        xterm_cmd.append('-hold')
    xterm_cmd.extend(['-e', cmd])

<<<<<<< HEAD
>>>>>>> 8739a86 (merge and number of bands fixed)
    result = subprocess.run(cmd, shell=True, check=False)
=======
    result = subprocess.run(xterm_cmd, check=False)
>>>>>>> 80e689e (Optimize mowing UDF and add local benchmark workflow)
=======
        print("`hold=True` requested. Command output will stay in the current terminal.")
    result = subprocess.run(cmd, shell=True, check=False)
>>>>>>> e1afd9e (Integrate tilewise mowing postprocessing)
=======
        xterm_cmd.append('-hold')
    xterm_cmd.extend(['-e', cmd])

    result = subprocess.run(xterm_cmd, check=False)
>>>>>>> 24c0c30 (second commit)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}")


<<<<<<< HEAD
def execute_cmd(hold, local_dir, force_dir, base_path, project_name, basename):
    cmd = (
        f'sudo docker run -v {local_dir} -v {force_dir} -u "$(id -u):$(id -g)" davidfrantz/force '
        "force-higher-level "
        f"{base_path}/process/temp/{project_name}/FORCE/{basename}/tsa_UDF.prm"
    )
    run_shell_command(cmd, hold=hold)


def mosaic_rasters(
    base_path,
    project_name,
    basename,
    aoi_path=None,
    dtype="uint16",
    band_indexes=None,
    output_filename=None,
):
<<<<<<< HEAD
<<<<<<< HEAD
=======
    """
    Mosaic rasters, optionally clip using AOI shapefile, and export with compression and compact dtype.
    Shows progress bars and step timings.
    """

    start_total = time.time()

    # Step 1: Find input raster files
    input_paths = glob.glob(f"{base_path}/process/temp/{project_name}/FORCE/{basename}/tiles_tss/X**/*.tif", recursive=True)
    print(f"Found {len(input_paths)} raster tiles.")
    if not input_paths:
        raise ValueError("No input .tif files found! Check your path.")

    # Step 2: Read rasters with progress bar
    src_files_to_mosaic = []
    start_read = time.time()
    for fp in tqdm(input_paths, desc="Reading raster tiles", unit="tile"):
        src_files_to_mosaic.append(rasterio.open(fp))
    end_read = time.time()
    print(f"✔ Finished reading in {end_read - start_read:.2f} seconds.")

>>>>>>> 24c0c30 (second commit)
    if band_indexes is None:
        band_indexes = list(range(1, src_files_to_mosaic[0].count + 1))

    single_source = src_files_to_mosaic[0] if len(src_files_to_mosaic) == 1 else None

    # Step 3: Load data or mosaic the rasters
    start_merge = time.time()
    if single_source is not None and aoi_path:
        print("📐 Clipping single raster with AOI...")
        aoi_gdf = gpd.read_file(aoi_path)
        if aoi_gdf.crs != single_source.crs:
            aoi_gdf = aoi_gdf.to_crs(single_source.crs)
        shapes = [geom.__geo_interface__ for geom in aoi_gdf.geometry]
        mosaic, out_transform = mask(single_source, shapes=shapes, crop=True, indexes=band_indexes)
        print(f"✔ Single-raster clip finished in {time.time() - start_merge:.2f} seconds.")
        aoi_path = None
    elif single_source is not None:
        print("⏭ Single raster input, skipping merge.")
        mosaic = single_source.read(indexes=band_indexes)
        out_transform = single_source.transform
        print(f"✔ Loaded single raster in {time.time() - start_merge:.2f} seconds.")
    else:
        print("🔄 Merging rasters...")
        mosaic, out_transform = merge(src_files_to_mosaic, indexes=band_indexes)
        print(f"✔ Merged in {time.time() - start_merge:.2f} seconds.")

    # Step 4: Prepare metadata
    out_meta = src_files_to_mosaic[0].meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "count": len(band_indexes),
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_transform,
        "compress": "deflate",
        "predictor": 2,
        "zlevel": 6,
        "dtype": dtype
    })

    # Step 5: Clip with AOI if provided
    if aoi_path:
        print("📐 Clipping mosaic with AOI...")
        start_clip = time.time()
        aoi_gdf = gpd.read_file(aoi_path)
        if aoi_gdf.crs != out_meta["crs"]:
            aoi_gdf = aoi_gdf.to_crs(out_meta["crs"])
        shapes = [geom.__geo_interface__ for geom in aoi_gdf.geometry]

        # Write to memory and re-open to clip the entire mosaic
        with MemoryFile() as memfile:
            with memfile.open(**out_meta) as temp_ds:
                temp_ds.write(mosaic)
            with memfile.open() as temp_ds:
                mosaic, out_transform = mask(dataset=temp_ds, shapes=shapes, crop=True)

        out_meta.update({
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": out_transform
        })
        end_clip = time.time()
        print(f"✔ Clipped in {end_clip - start_clip:.2f} seconds.")

    # Step 6: Set up output
    output_dir = f"{base_path}/process/results/{project_name}"
    os.makedirs(output_dir, exist_ok=True)
    if output_filename is None:
        first_name = os.path.splitext(os.path.basename(input_paths[0]))[0]
        output_filename = os.path.join(output_dir, f"{first_name}.tif")

    # Step 7: Prepare band descriptions
    source_descriptions = src_files_to_mosaic[0].descriptions
    descriptions = [source_descriptions[index - 1] for index in band_indexes]
    if descriptions and all(desc is not None for desc in descriptions):
        out_meta["descriptions"] = tuple(descriptions)

    # Step 8: Write mosaic and set band descriptions
    print("💾 Saving mosaic to disk...")
    start_write = time.time()
    with rasterio.open(output_filename, "w", **out_meta) as dest:
        dest.write(mosaic)
        for i, desc in tqdm(enumerate(descriptions, 1), total=len(descriptions), desc="Setting band descriptions"):
            dest.set_band_description(i, desc)
    end_write = time.time()
    print(f"✔ Saved in {end_write - start_write:.2f} seconds.")

    # Step 9: Close all rasters
    for src in src_files_to_mosaic:
        src.close()

    end_total = time.time()
    print(f"\n🎉 Mosaic saved to: {output_filename}")
    print(f"⏱ Total time: {end_total - start_total:.2f} seconds")

    return output_filename


def export_selected_mowing_bands(base_path, project_name, basename, aoi_path=None):
    selected_band_indexes = [1, 5, 6, 7, 8, 9, 10, 11]
    output_filename = os.path.join(
        base_path,
        "process",
        "results",
        project_name,
        f"mowing-events_{os.path.splitext(basename)[0]}.tif",
        #f"mowing_events_{os.path.splitext(basename)[0]}.tif",
    )

    return mosaic_rasters(
        base_path=base_path,
        project_name=project_name,
        basename=basename,
        aoi_path=aoi_path,
        dtype="int16",
        band_indexes=selected_band_indexes,
        output_filename=output_filename,
    )
=======
=======
>>>>>>> 8739a86 (merge and number of bands fixed)
def execute_cmd(hold, local_dir, force_dir, base_path, project_name, basename):
    cmd = (
        f'sudo docker run -v {local_dir} -v {force_dir} -u "$(id -u):$(id -g)" davidfrantz/force '
        "force-higher-level "
        f"{base_path}/process/temp/{project_name}/FORCE/{basename}/tsa_UDF.prm"
    )
    run_shell_command(cmd, hold=hold)


<<<<<<< HEAD
    if hold == True:
        subprocess.run(['xterm', '-hold', '-e', cmd])
    else:
        subprocess.run(['xterm','-e', cmd])
<<<<<<< HEAD
>>>>>>> 89c9170 (version 0.1)
=======


def mosaic_rasters(base_path, project_name, basename, aoi_path=None, dtype="uint16"):
=======
def mosaic_rasters(
    base_path,
    project_name,
    basename,
    aoi_path=None,
    dtype="uint16",
    band_indexes=None,
    output_filename=None,
):
>>>>>>> 8739a86 (merge and number of bands fixed)
    """
    Mosaic rasters, optionally clip using AOI shapefile, and export with compression and compact dtype.
    Shows progress bars and step timings.
    """

    start_total = time.time()

    # Step 1: Find input raster files
    input_paths = glob.glob(f"{base_path}/process/temp/{project_name}/FORCE/{basename}/tiles_tss/X**/*.tif", recursive=True)
    print(f"Found {len(input_paths)} raster tiles.")
    if not input_paths:
        raise ValueError("No input .tif files found! Check your path.")

    # Step 2: Read rasters with progress bar
    src_files_to_mosaic = []
    start_read = time.time()
    for fp in tqdm(input_paths, desc="Reading raster tiles", unit="tile"):
        src_files_to_mosaic.append(rasterio.open(fp))
    end_read = time.time()
    print(f"✔ Finished reading in {end_read - start_read:.2f} seconds.")

=======
>>>>>>> e1afd9e (Integrate tilewise mowing postprocessing)
    if band_indexes is None:
        band_indexes = DEFAULT_BANDS.copy()

    base_path_obj = Path(base_path)
    basename_stem = Path(basename).stem
    results_dir = base_path_obj / "process" / "results" / project_name

    if output_filename is None:
        final_output_path = results_dir / f"mowing-events_{basename_stem}.tif"
    else:
        final_output_path = Path(output_filename)

    output_dir = final_output_path.parent / f"{final_output_path.stem}_tiles"
    vrt_output_path = final_output_path.with_suffix(".vrt")
    report_path_obj = Path(report_path) if report_path else final_output_path.with_name(
        f"{final_output_path.stem}_report.json"
    )

    _, final_vrt, final_raster = export_tiles(
        base_path=base_path_obj,
        project_name=project_name,
        basename=basename,
        output_dir=output_dir,
        vrt_output_path=None if skip_vrt else vrt_output_path,
        final_output_path=None if skip_final_raster else final_output_path,
        band_indexes=band_indexes,
        aoi_path=Path(aoi_path) if aoi_path else None,
        dtype=dtype,
        num_threads=num_threads,
        cachemax_mb=cachemax_mb,
        skip_vrt=skip_vrt,
        skip_final_raster=skip_final_raster,
        overwrite_tiles=overwrite_tiles,
        build_overviews=build_overviews,
        overview_resampling=overview_resampling,
        report_path=report_path_obj,
        compression_method=compression_method,
        bigtiff=bigtiff,
        zlevel=zlevel,
        blocksize=blocksize,
        output_nodata=output_nodata,
        fallback_nodata=fallback_nodata,
    )

    if final_raster is not None:
        return str(final_raster)
    if final_vrt is not None:
        return str(final_vrt)
    return str(output_dir)


def export_selected_mowing_bands(base_path, project_name, basename, aoi_path=None):
    output_filename = os.path.join(
        base_path,
        "process",
        "results",
        project_name,
        f"mowing-events_{os.path.splitext(basename)[0]}.tif",
    )

    return mosaic_rasters(
        base_path=base_path,
        project_name=project_name,
        basename=basename,
        aoi_path=aoi_path,
        dtype="int16",
        band_indexes=DEFAULT_BANDS,
        output_filename=output_filename,
    )
<<<<<<< HEAD




>>>>>>> 00bcb7d (Mosaic step)
=======
>>>>>>> 80e689e (Optimize mowing UDF and add local benchmark workflow)
