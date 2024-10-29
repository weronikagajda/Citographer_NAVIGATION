import addon_utils #to activate a check function
import os
import bpy

def enable_addon(addon_name):
    # check if the addon is enabled
    loaded_default, loaded_state = addon_utils.check(addon_name)
    if not loaded_state:
        # enable the addon
        addon_utils.enable(addon_name)
    return {'FINISHED'} 

def update_camera_ortho_scale(self, context):
    cam = context.scene.camera
    if cam and cam.type == 'CAMERA' and cam.data.type == 'ORTHO':
        cam.data.ortho_scale = context.scene.camera_ortho_scale

def update_camera_z_position(self, context):
    cam = context.scene.camera
    if cam and cam.type == 'CAMERA':
        cam.location.z = context.scene.camera_z_position

def update_camera_rotation(self, context):
    cam = context.scene.camera
    if cam and cam.type == 'CAMERA':
        cam.rotation_euler[2] = context.scene.camera_rotation  # Z-axis rotation
        
def zoom_update(self, context):
    # Check if a camera named "Cito_iPhone_Camera" exists
    cam = bpy.context.scene.camera
    if cam and "Cito_iPhone_Camera" in cam.name:
        if bpy.context.scene.iphone_camera_zoom_mode == 'WIDE':
            cam.data.lens = bpy.context.scene.iphone_camera_wide_zoom
        elif bpy.context.scene.iphone_camera_zoom_mode == 'ULTRA_WIDE':
            cam.data.lens = bpy.context.scene.iphone_camera_ultra_wide_zoom
        elif bpy.context.scene.iphone_camera_zoom_mode == 'TELEPHOTO':
            cam.data.lens = bpy.context.scene.iphone_camera_telephoto_zoom
