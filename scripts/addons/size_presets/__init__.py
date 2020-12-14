import bpy
import os
import json


bl_info = {
    "name" : "Grease Pencil Brush/Size Presets",
    "auther": "Shintaro Ishimine",
    "description": "Select grease pencil brush size from presets.",
    "version": (1, 0, 0),
    "blender": (2, 91, 0),
    "location": "Properties > Active Tool and Workspace Settigns > Size Presets",
    "category": "Paint"
}


class View3DPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)


class GreasePencilPaintPanel:
    bl_context = ".greasepencil_paint"
    bl_category = "Tool"

    @classmethod
    def poll(cls, context):
        if context.space_data.type in {"VIEW_3D", "PROPERTIES"}:
            if context.gpencil_data is None:
                return False
            return bool(context.gpencil_data.is_stroke_paint_mode)
        else:
            return True


class VIEW3D_PT_tools_grease_pencil_radius_select(bpy.types.Panel, View3DPanel, GreasePencilPaintPanel):
    bl_context = ".greasepencil_paint"
    bl_label = "Radius Presets"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        brush = context.scene.tool_settings.gpencil_paint.brush

        row = layout.row()
        row.column().template_icon_view(brush, "size_preset", show_labels=True)
        row.column().menu("VIEW3D_MT_brush_gpencil_context_menu", icon="DOWNARROW_HLT", text="")
        layout.row().prop(brush, "size", text="Radius")
            

global_store = {}


def load_presets(presets_location):
    presets_path = os.path.join(presets_location, "presets.json")
    pcoll = bpy.utils.previews.new()
    with open(presets_path) as f:
        presets = json.load(f)
    global_store["presets"] = presets
    image_location = os.path.join(presets_location, "icons")
    items = []
    for i, key in enumerate(presets.keys()):
        preset = presets[key]
        filepath = os.path.join(image_location, preset["icon_file"])
        thumb = pcoll.load(filepath, filepath, "IMAGE")
        items.append((key, key, "", thumb.icon_id, i))
    global_store["pcoll"] = pcoll
    return items

def update_presets(self, context):
    brush = context.scene.tool_settings.gpencil_paint.brush
    size = global_store["presets"][brush.size_preset]["size"]
    brush.size = size

def register():
    presets_location = os.path.join(os.path.dirname(__file__), "presets")
    # presets_location = bpy.path.abspath("//presets")
    items = load_presets(presets_location)
    bpy.types.Brush.size_preset = bpy.props.EnumProperty(items=items, update=update_presets)
    bpy.utils.register_class(VIEW3D_PT_tools_grease_pencil_radius_select)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_tools_grease_pencil_radius_select)
    bpy.utils.previews.remove(global_store["pcoll"])
    global_store.clear()
    del bpy.types.Brush.size_preset

if __name__ == "__main__":
    register()
