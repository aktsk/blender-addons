bl_info = {
    "name" : "undoWithoutCamera",
    "author": "takanakahiko(aktsk)",
    "version": (1, 0),
    "blender": (2, 91, 0),
    "location": "",
    "description": "redo時も反転状態を維持するやつ",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

import bpy

scale_x = 1

def handler_undo_pre(scene):
    print('pre')
    global scale_x
    scale_x = bpy.data.objects['Camera'].scale.x

def handler_undo_post(scene):
    print('post')
    if bpy.data.objects['Camera'].scale.x != scale_x :
        bpy.data.objects['Camera'].scale.x = scale_x
        bpy.ops.ed.undo()

def register():
    print("register")
    bpy.app.handlers.undo_pre.append(handler_undo_pre)
    bpy.app.handlers.undo_post.append(handler_undo_post)

def unregister():
    print("unregister")
    bpy.app.handlers.undo_pre.remove(handler_undo_pre)
    bpy.app.handlers.undo_post.remove(handler_undo_post)

if __name__ == "__main__":
    register()
