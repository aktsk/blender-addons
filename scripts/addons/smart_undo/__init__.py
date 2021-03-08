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

# 機能の有効化と無効化を切り替える Operator
class SwitchEnabled(bpy.types.Operator):
    bl_idname = "smart_undo.switch_enabled"
    bl_label = "Switch enabled (Smart Undo)"
    
    def execute(self, context):
        preferences = context.preferences.addons[__name__].preferences
        preferences.enabled = not preferences.enabled
        SmartUndoUI.redraw()
        return{'FINISHED'}


# Undo 前にカメラの反転や回転の状態を記録する
@bpy.app.handlers.persistent
def handler_undo_pre(scene):
    vars(handler_undo_pre)["scale.x"] = scene.camera.scale.x
    vars(handler_undo_pre)["rotation_euler.y"] = scene.camera.rotation_euler.y


# Undo 後にもしカメラが変化していたらもとに戻す（Undoしても変わってないように見える）
@bpy.app.handlers.persistent
def handler_undo_post(scene):

    # 有効化されていなかったら処理を中止する
    preferences = bpy.context.preferences.addons[__name__].preferences
    if not preferences.enabled:
        return

    scale_x = vars(handler_undo_pre)["scale.x"]
    if scene.camera.scale.x != scale_x :
        scene.camera.scale.x = scale_x
        # bpy.ops.ed.undo() # 反転作業がヒストリに記録されているならこの処理が必要となる

    rotation_euler_y = vars(handler_undo_pre)["rotation_euler.y"]
    if scene.camera.rotation_euler.y != rotation_euler_y :
        scene.camera.rotation_euler.y = rotation_euler_y
        # bpy.ops.ed.undo() # 回転作業がヒストリに記録されているならこの処理が必要となる


class SMART_UNDO_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    enabled : bpy.props.BoolProperty(default=True, name = "enabled", description = "enabled")
    def draw(self, context):
        self.layout.prop(self, "enabled")


class SmartUndoUI(bpy.types.Panel):
    bl_label = "Smart Undo"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Smart Undo"
  
    def draw(self, context):
        preferences = context.preferences.addons[__name__].preferences
        if preferences.enabled:
            self.layout.operator(SwitchEnabled.bl_idname, text="無効にする")
        else:
            self.layout.operator(SwitchEnabled.bl_idname, text="有効にする")
    
    @staticmethod
    def redraw():
        try:
            bpy.utils.unregister_class(SmartUndoUI)
        except:
            pass
        bpy.utils.register_class(SmartUndoUI)


classes = [ SMART_UNDO_AddonPreferences, SmartUndoUI, SwitchEnabled ]


def register():
    print("register smart_undo")

    for c in classes:
        bpy.utils.register_class(c)
    
    bpy.app.handlers.undo_pre.append(handler_undo_pre)
    bpy.app.handlers.undo_post.append(handler_undo_post)

    bpy.app.handlers.redo_pre.append(handler_undo_pre)
    bpy.app.handlers.redo_post.append(handler_undo_post)

def unregister():
    print("unregister smart_undo")

    for c in reversed(classes):
        bpy.utils.unregister_class(c)

    bpy.app.handlers.undo_pre.remove(handler_undo_pre)
    bpy.app.handlers.undo_post.remove(handler_undo_post)

    bpy.app.handlers.redo_pre.remove(handler_undo_pre)
    bpy.app.handlers.redo_post.remove(handler_undo_post)


if __name__ == "__main__":
    register()
