bl_info = {
    "name" : "Smart Undo",
    "author": "takanakahiko(aktsk)",
    "version": (1, 0),
    "blender": (2, 91, 0),
    "location": "",
    "description": "Undo 時も反転や回転の状態を維持します",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

import bpy

class SMART_UNDO_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    enabled : bpy.props.BoolProperty(default=True, name = "enabled", description = "enabled")
    def draw(self, context):
        self.layout.prop(self, "enabled")

class UI(bpy.types.Panel):
    bl_label = "Smart Undo"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Smart Undo"
  
    def draw(self, context):
        preferences = context.preferences.addons[__name__].preferences
        if preferences.enabled:
            self.layout.operator(EnableButton.bl_idname, text="無効にする")
        else:
            self.layout.operator(EnableButton.bl_idname, text="有効にする")


class EnableButton(bpy.types.Operator):
    bl_idname = "enable.button"
    bl_label = "eneble"
    
    def execute(self, context):
        preferences = context.preferences.addons[__name__].preferences
        preferences.enabled = not preferences.enabled
        if preferences.enabled:
            self.bl_label = "無効にする"
        else:
            self.bl_label = "有効にする"
        return{'FINISHED'}


@bpy.app.handlers.persistent
def handler_undo_pre(scene):
    print('undo_pre')

    vars(handler_undo_pre)["scale.x"] = scene.camera.scale.x
    vars(handler_undo_pre)["rotation_euler.y"] = scene.camera.rotation_euler.y


@bpy.app.handlers.persistent
def handler_undo_post(scene):
    print('undo_post')

    preferences = bpy.context.preferences.addons[__name__].preferences
    if not preferences.enabled:
        return

    scale_x = vars(handler_undo_pre)["scale.x"]
    if scene.camera.scale.x != scale_x :
        scene.camera.scale.x = scale_x
        bpy.ops.ed.undo() # 反転方法によって、この処理が必要でない可能性がある

    rotation_euler_y = vars(handler_undo_pre)["rotation_euler.y"]
    if scene.camera.rotation_euler.y != rotation_euler_y :
        scene.camera.rotation_euler.y = rotation_euler_y
        bpy.ops.ed.undo() # 反転方法によって、この処理が必要でない可能性がある

classes = [ SMART_UNDO_AddonPreferences, UI, EnableButton ]

def register():
    print("register")

    for c in classes:
        bpy.utils.register_class(c)
    
    bpy.app.handlers.undo_pre.append(handler_undo_pre)
    bpy.app.handlers.undo_post.append(handler_undo_post)
    bpy.app.handlers.redo_pre.append(handler_undo_pre)
    bpy.app.handlers.redo_post.append(handler_undo_post)

def unregister():
    print("unregister")

    for c in reversed(classes):
        bpy.utils.unregister_class(c)

    bpy.app.handlers.undo_pre.remove(handler_undo_pre)
    bpy.app.handlers.undo_post.remove(handler_undo_post)
    bpy.app.handlers.redo_pre.remove(handler_undo_pre)
    bpy.app.handlers.redo_post.remove(handler_undo_post)

if __name__ == "__main__":
    register()
