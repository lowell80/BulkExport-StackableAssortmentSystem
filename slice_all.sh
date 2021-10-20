
# https://github.com/theskyishard/prusaslicer-command-line-helper
# https://forum.prusaprinters.org/forum/prusaslicer/running-prusaslicer-in-batch-command-line-mode-mixing-configurations-for-fff-and-sla-technologies/#post-145142
# https://projects.ttlexceeded.com/3dprinting_prusaslicer_batch.html
#


# Slic3r references:
# https://manual.slic3r.org/advanced/command-line
# https://subscription.packtpub.com/book/hardware-and-creative/9781783284979/1/ch01lvl1sec14/running+slic3r+from+the+command+line+(become+an+expert)



/Applications/PrusaSlicer.app/Contents/MacOS/PrusaSlicer \
  --load "/Users/lalleman/Library/Application Support/PrusaSlicer/vendor/PrusaResearch.ini" \
  --printer-technology FFF \
  --export-gcode --slice \
  --load "/Users/lalleman/Library/Application Support/PrusaSlicer/PrusaSlicer.ini" \
  --preset-name MK3S \
  "/Users/lalleman/Dropbox/3D Prints/F360_Exports/Stackable-Assortment-System/box-1x1-1u_base-25_grid-49.stl" \
  --output "/tmp/{input_filename_base}_{layer_height}mm_{filament_type[0]}_{printer_model}_{print_time}.gcode"





/Applications/PrusaSlicer.app/Contents/MacOS/PrusaSlicer \
  --load "/Users/lalleman/Library/Application Support/PrusaSlicer/vendor/PrusaResearch.ini" \
  --printer-technology FFF \
  --export-gcode \
  --load "printer/Original Prusa i3 MK3S - With Octoprint.ini" \
  --preset-name MK3S \
  --slice "/Users/lalleman/Dropbox/3D Prints/F360_Exports/Stackable-Assortment-System/box-1x1-1u_base-25_grid-49.stl"





/Applications/PrusaSlicer.app/Contents/MacOS/PrusaSlicer \
  --load "/Users/lalleman/Library/Application Support/PrusaSlicer/vendor/PrusaResearch.ini" \
  --printer-technology FFF  --center 125,105 \
  --load "printer/Original Prusa i3 MK3S - With Octoprint.ini" \
  --preset-name MK3S \
  --export-3mf \
  "/Users/lalleman/Dropbox/3D Prints/F360_Exports/Stackable-Assortment-System/box-1x1-1u_base-25_grid-49.stl"








# Attempts to use variable names in the output file seem to also fail:

	--output "/tmp/{input_filename_base}_{layer_height}mm_{filament_type[0]}_{printer_model}_{print_time}.gcode
