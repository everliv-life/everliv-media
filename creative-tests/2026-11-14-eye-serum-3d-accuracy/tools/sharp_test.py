import sys, os
INTERP = os.environ.get('INTERP', 'Cubic'); FW = float(os.environ.get('FW', '0.8'))
exec(open('build_eye_serum.py').read().replace("bpy.ops.render.render(write_still=True)\nbpy.ops.wm.save_as_mainfile(filepath=OUT + '.blend')",
 "pass").replace("tex.interpolation = 'Cubic'", "tex.interpolation = INTERP").replace("sc.cycles.filter_width = 0.8", "sc.cycles.filter_width = FW"))
sc.render.use_border = True; sc.render.use_crop_to_border = True
sc.render.border_min_x, sc.render.border_max_x = 860/2048, 1180/2048
sc.render.border_min_y, sc.render.border_max_y = 1 - 1700/2048, 1 - 820/2048
bpy.ops.render.render(write_still=True)
