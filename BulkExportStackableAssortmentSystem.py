#Author-Lowell
#Description-

import traceback
from itertools import combinations_with_replacement
from pathlib import Path

import adsk.cam
import adsk.core
import adsk.fusion

base_export = Path("~/Dropbox/3D Prints/F360_Exports").expanduser()

highest_size = 4
highest_unit = 2







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

        # Specify the folder to write out the results.
        folder = base_export / "Stackable-Assortment-System"
        folder.mkdir(exist_ok=True)

        # Changing params
        segments_x_param = get_param('BoxSegmentsX')
        segments_y_param = get_param('BoxSegmentsY')
        segments_u_param = get_param('BoxHeightUnits')


        # Params for base filename:
        segment_size_x = param_value("SegmentSizeX")
        box_height_base = param_value("BoxHeightBase")
        lid_height_base = param_value("LidHeightBase")

        for x, y in combinations_with_replacement(range(1, highest_size+1), 2):
            segments_x_param.expression = str(x)
            segments_y_param.expression = str(y)

            export_component(design, lid_component,
                                folder / f"lid-{x}x{y}-lid-{lid_height_base}_grid-{segment_size_x}.stl")

            for u in range(1, highest_unit + 1):
                segments_u_param.expression = str(u)

                # Let the view have a chance to paint just so you can watch the progress.
                adsk.doEvents()

                export_component(design, box_component,
                                folder / f"box-{x}x{y}-{u}u_base-{box_height_base}_grid-{segment_size_x}.stl")
        # Restore param values back to their original values

        ui.messageBox('Finished.')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
