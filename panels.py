import bpy
from bpy.types import Panel
from .operators import *
from .utilities import *

class Panel_PT_CitoAddCamera(bpy.types.Panel):
    bl_label = "CITOGRAPHY - Camera"
    bl_idname = "C_PT_CitoAddCamera"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cito CAMERA"
    bl_context = "objectmode"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        # Adding pink-like text and icons
        layout.label(text="Add Your Camera!", icon="COLOR")  # Pink hint with "COLOR" icon
        layout.operator("view3d.add_camera_scaled_up", text="Add Camera 🎥", icon="CAMERA_DATA")
        layout.operator("view3d.cito_view_selected_camera", text="View from Selected Camera", icon="OUTLINER_DATA_CAMERA")

class Panel_PT_CitographyExploreFrame(Panel):
    bl_label = "CITOGRAPHY - Image"
    bl_idname = "C_PT_CitoImportExploreFrame"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cito CAMERA"
    bl_context = "objectmode"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Options", icon="RESTRICT_RENDER_OFF")

class Panel_PT_CitographyExploreAnimation(Panel):
    bl_label = "CITOGRAPHY - Animation"
    bl_idname = "C_PT_CitoExploreAnimation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cito CAMERA"
    bl_context = "objectmode"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Animation Settings", icon="FILE_MOVIE")

class SubPanel_PT_OrthoCamera(Panel):
    bl_label = "📸 ORTHO CAMERA:"
    bl_idname = "C_PT_CitoImagePanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Cito CAMERA"
    bl_parent_id = "C_PT_CitoImportExploreFrame"
    bl_options = {"DEFAULT_CLOSED"} 
    
    def draw(self, context):
        layout = self.layout
        layout.operator("view3d.add_camera_section_ortho", text="Add Section-Ortho Camera", icon="CAMERA_DATA")
        layout.operator("view3d.add_camera_top_view_ortho", text="Add Top-Ortho Camera", icon="CAMERA_DATA")
        layout.prop(context.scene, "camera_ortho_scale", text="Ortho Scale")
        layout.prop(context.scene, "camera_z_position", text="Z Position")
        layout.prop(context.scene, "camera_rotation", text="Rotation")

class SubPanel_PT_IphoneCamera(bpy.types.Panel):
    bl_label = "📱 IPHONE CAMERA:"
    bl_idname = "C_PT_CitoGeoLocPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Cito CAMERA"
    bl_parent_id = "C_PT_CitoImportExploreFrame"  
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Add iPhone camera with icon
        layout.operator("view3d.add_iphone_camera", text="Add iPhone Camera 📱", icon="CAMERA_DATA")
        layout.operator("view3d.toggle_iphone_camera_orientation", text="Toggle Orientation", icon="ORIENTATION_LOCAL")
        
        # Zoom mode dropdown with label
        layout.prop(scene, "iphone_camera_zoom_mode", text="Zoom Mode")

        # Display appropriate zoom slider based on selected zoom mode
        if scene.iphone_camera_zoom_mode == 'WIDE':
            layout.prop(scene, "iphone_camera_wide_zoom", text="Wide Zoom (26mm)")
        elif scene.iphone_camera_zoom_mode == 'ULTRA_WIDE':
            layout.prop(scene, "iphone_camera_ultra_wide_zoom", text="Ultra-Wide Zoom (13mm)")
        elif scene.iphone_camera_zoom_mode == 'TELEPHOTO':
            layout.prop(scene, "iphone_camera_telephoto_zoom", text="Telephoto Zoom (65mm)")

class SubPanel_PT_RenderFrame(Panel):
    bl_label = "🎬 RENDER:"
    bl_idname = "C_PT_CitoStartPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Cito CAMERA"
    bl_parent_id = "C_PT_CitoImportExploreFrame"  
    bl_options = {"DEFAULT_CLOSED"} 
    
    def draw(self, context):
        layout = self.layout
        layout.operator("view3d.cito_render_viewport", text="Render Viewport Image", icon="RENDER_STILL")
        layout.prop(context.scene.render, "film_transparent", text="Transparent Background")
        layout.label(text="Resolution:", icon="IMAGE_DATA")
        layout.prop(context.scene.render, "resolution_x", text="Resolution X")
        layout.prop(context.scene.render, "resolution_y", text="Resolution Y")

class SubPanel_PT_CircularPath(Panel):
    bl_label = "🔄 CIRCULAR PATH:"
    bl_idname = "C_PT_CitocCircularAnimation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Cito CAMERA"
    bl_parent_id = "C_PT_CitoExploreAnimation"  
    bl_options = {"DEFAULT_CLOSED"} 
    
    def draw(self, context):
        layout = self.layout
        layout.operator("view3d.cito_create_animation_setup", text="Create Animation Setup", icon="OUTLINER_DATA_CAMERA")
        layout.operator("object.animate_follow_path", text="Animate Path", icon="RENDER_ANIMATION")

class SubPanel_PT_SelectedPath(Panel):
    bl_label = "📐 SELECTED PATH:"
    bl_idname = "C_PT_CitocPathAnimation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Cito CAMERA"
    bl_parent_id = "C_PT_CitoExploreAnimation"  
    bl_options = {"DEFAULT_CLOSED"} 
    
    def draw(self, context):
        layout = self.layout
        layout.operator("view3d.use_selected_nurbs_to_animate_camera", text="Selected Path Animation", icon="CURVE_NCURVE")
        layout.operator("object.animate_nurbs_path", text="Animate Path", icon="ANIM")

class SubPanel_PT_RenderAnimation(Panel):
    bl_label = "🎥 RENDER ANIMATION:"
    bl_idname = "C_PT_CitocRenderAnimation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Cito CAMERA"
    bl_parent_id = "C_PT_CitoExploreAnimation"  
    bl_options = {"DEFAULT_CLOSED"} 
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Directory selection for output frames
        layout.prop(scene, "frame_output_directory", text="Output Folder")

        # Dropdown for output type (Frames or AVI)
        layout.prop(scene, "animation_output_type", text="Output Type")
        
        # Button to trigger viewport render animation
        layout.operator("view3d.cito_viewport_render_animation", text="Render Animation", icon="RENDER_ANIMATION")

classes = [
    Panel_PT_CitoAddCamera,
    Panel_PT_CitographyExploreFrame,
    SubPanel_PT_OrthoCamera,
    SubPanel_PT_IphoneCamera,
    SubPanel_PT_RenderFrame,
    Panel_PT_CitographyExploreAnimation,
    SubPanel_PT_CircularPath,
    SubPanel_PT_SelectedPath,
    SubPanel_PT_RenderAnimation,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
