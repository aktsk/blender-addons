
bl_info = {
    "name" : "Grease Pencil Brush/Size Presets",
    "description": "Select grease pencil brush size from presets.",
    "version": (1, 0, 0),
    "blender": (2, 9, 1),
    "location": "Properties > Active Tool and Workspace Settigns > Size Presets"
    "category": "Paint"
}

from bpy.types import Panel
from bl_ui.utils import PresetPanel
    

class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

class GreasePencilPaintPanel:
    bl_context = ".greasepencil_paint"
    bl_category = "Tool"

    @classmethod
    def poll(cls, context):
        if context.space_data.type in {'VIEW_3D', 'PROPERTIES'}:
            if context.gpencil_data is None:
                return False

            gpd = context.gpencil_data
            return bool(gpd.is_stroke_paint_mode)
        else:
            return True

class VIEW3D_PT_tools_grease_pencil_radius_select(Panel, View3DPanel, GreasePencilPaintPanel):
    bl_context = ".greasepencil_paint"
    bl_label = "Radius Presets"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        tool_settings = context.scene.tool_settings
        gpencil_paint = tool_settings.gpencil_paint

        row = layout.row()
        row.column().template_ID_preview(gpencil_paint, "brush", new="brush.scale_size", rows=3, cols=8)

        col = row.column()
        col.menu("VIEW3D_MT_brush_gpencil_context_menu", icon='DOWNARROW_HLT', text="")

        if context.mode == 'PAINT_GPENCIL':
            brush = gpencil_paint.brush
            if brush is not None:
                layout.row().prop(brush, "size", text="Radius")

def register():
    from bpy.utils import register_class
    register_class(VIEW3D_PT_tools_grease_pencil_radius_select)

def unregister():
    pass
