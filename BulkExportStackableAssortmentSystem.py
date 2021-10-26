#Author-Lowell
#Description-

import traceback
from contextlib import contextmanager
from itertools import combinations_with_replacement
from pathlib import Path

import adsk.cam
import adsk.core
import adsk.fusion

base_export = Path("~/Dropbox/3D Prints/F360_Exports").expanduser()

highest_size = 4
highest_unit = 2
highest_grid = 6


@contextmanager
def get_reverting_param(design, name : str):
    """ This context manager restores the original values of a paramater once we
    are done varying it. """
    param = design.allParameters.itemByName(name)
    expression = param.expression
    try:
        yield param
    finally:
        # Reset to the original value
        param.expression = expression





def export_component(design, component, filename):
    # Save the file as STL.
    exportMgr = adsk.fusion.ExportManager.cast(design.exportManager)
    stlOptions = exportMgr.createSTLExportOptions(component)
    stlOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
    stlOptions.filename = str(filename)
    exportMgr.execute(stlOptions)

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)

        # Avoid some verbosity..
        def get_param(name : str):
            return design.allParameters.itemByName(name)

        def param_value(name : str):
            # Drop units (mm)
            v = get_param(name).expression
            return v.split(" ")[0]

        # Get the root component of the active design
        # rootComp = design.rootComponent

        box_component = next(c for c in design.allComponents if c.name == "Box")
        lid_component = next(c for c in design.allComponents if c.name == "Lid")
        grid_component = next(c for c in design.allComponents if c.name == "Grid")

        # Specify the folder to write out the results.
        folder = base_export / "Stackable-Assortment-System"
        folder.mkdir(exist_ok=True)

        # Static params (used in output file name)  (database unit is cm, we want mm)
        segment_size_x = int(get_param("SegmentSizeX").value * 10)
        segment_size_y = int(get_param("SegmentSizeY").value * 10)
        box_height_base = int(get_param("BoxHeightBase").value * 10)
        lid_height_base = int(get_param("LidHeightBase").value * 10)

        if segment_size_x == segment_size_y:
            segment_size = segment_size_x
            is_square = True
        else:
            segment_size = f"{segment_size_x}x{segment_size_y}"
            is_square = False

        with get_reverting_param(design, "BoxSegmentsX") as segments_x_param, \
             get_reverting_param(design, "BoxSegmentsY") as segments_y_param, \
             get_reverting_param(design, "BoxHeightUnits") as segments_u_param:

            for x, y in combinations_with_replacement(range(1, highest_size+1), 2):
                segments_x_param.expression = str(x)
                segments_y_param.expression = str(y)

                export_component(design, lid_component,
                                 folder / f"lid-{x}x{y}-lid-{lid_height_base}_grid-{segment_size}.stl")

                for u in range(1, highest_unit + 1):
                    segments_u_param.expression = str(u)

                    # Let the view have a chance to paint just so you can watch the progress.
                    adsk.doEvents()

                    export_component(design, box_component,
                                    folder / f"box-{x}x{y}-{u}u_base-{box_height_base}_grid-{segment_size}.stl")

        # Make range of grid sizes

        with get_reverting_param(design, "GridSegmentsX") as grid_x_param, \
             get_reverting_param(design, "GridSegmentsY") as grid_y_param:

            # We are basically assuming that the grid is square here.
            # This (Otherwise 2x3 and 3x2 are NOT the same thing)
            assert is_square, "We didn't code for non-square grid generation yet"
            for x, y in combinations_with_replacement(range(1, highest_grid+1), 2):
                grid_x_param.expression = str(x)
                grid_y_param.expression = str(y)

                adsk.doEvents()
                export_component(design, grid_component,
                                 folder / f"grid-{x}x{y}_base-{box_height_base}_grid-{segment_size}.stl")


        adsk.doEvents()
        ui.messageBox('Finished.')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
