exec(open('build_eye_serum.py').read().replace("bpy.ops.render.render(write_still=True)\nbpy.ops.wm.save_as_mainfile(filepath=OUT + '.blend')","pass"))
sc.render.use_border = True; sc.render.use_crop_to_border = True
sc.render.border_min_x, sc.render.border_max_x = 780/2048, 1270/2048
sc.render.border_min_y, sc.render.border_max_y = 1 - 830/2048, 1 - 230/2048
bpy.ops.render.render(write_still=True)
