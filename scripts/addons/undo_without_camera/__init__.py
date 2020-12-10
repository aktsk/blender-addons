bl_info = {
    "name" : "undoWithoutCamera",
    "author": "takanakahiko(aktsk)",
    "version": (1, 0),
    "blender": (2, 91, 0),
    "location": "",
    "description": "redo時も反転や回転の状態を維持します",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

import bpy


@bpy.app.handlers.persistent
def handler_undo_pre(scene):
    print('undo_pre')

    vars(handler_undo_pre)["scale.x"] = scene.camera.scale.x
    vars(handler_undo_pre)["rotation_euler.y"] = scene.camera.rotation_euler.y


@bpy.app.handlers.persistent
def handler_undo_post(scene):
    print('undo_post')

    scale_x = vars(handler_undo_pre)["scale.x"]
    if scene.camera.scale.x != scale_x :
        scene.camera.scale.x = scale_x
        bpy.ops.ed.undo() # 反転方法によって、この処理が必要でない可能性がある

    rotation_euler_y = vars(handler_undo_pre)["rotation_euler.y"]
    if scene.camera.rotation_euler.y != rotation_euler_y :
        scene.camera.rotation_euler.y = rotation_euler_y
        bpy.ops.ed.undo() # 反転方法によって、この処理が必要でない可能性がある

def register():
    print("register")
    bpy.app.handlers.undo_pre.append(handler_undo_pre)
    bpy.app.handlers.undo_post.append(handler_undo_post)
    bpy.app.handlers.redo_pre.append(handler_undo_pre)
    bpy.app.handlers.redo_post.append(handler_undo_post)

def unregister():
    print("unregister")
    bpy.app.handlers.undo_pre.remove(handler_undo_pre)
    bpy.app.handlers.undo_post.remove(handler_undo_post)
    bpy.app.handlers.redo_pre.remove(handler_undo_pre)
    bpy.app.handlers.redo_post.remove(handler_undo_post)

if __name__ == "__main__":
    register()
