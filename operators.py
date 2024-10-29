import bpy
from bpy.types import Operator
from bpy.props import StringProperty, FloatProperty, IntProperty, EnumProperty
from .utilities import *

# Properties to register
properties = {
    "camera_ortho_scale": FloatProperty(
        name="Ortho Scale",
        description="Adjust the orthographic scale of the active camera",
        default=50.0,
        min=1.0,
        max=1000.0,
        update=update_camera_ortho_scale
    ),
    "camera_z_position": FloatProperty(
        name="Z Position",
        description="Move the camera along the Z-axis",
        default=0.0,
        min=-500.0,
        max=500.0,
        update=update_camera_z_position
    ),
    "camera_rotation": FloatProperty(
        name="Rotation",
        description="Rotate the camera around the Z-axis",
        default=0.0,
        min=-3.1416,  # -180 degrees
        max=3.1416,   # 180 degrees
        update=update_camera_rotation
    ),
    "iphone_camera_zoom_mode": EnumProperty(
        name="Zoom Mode",
        description="Choose zoom mode for the iPhone camera",
        items=[
            ('WIDE', "Wide (26mm)", "Standard wide lens"),
            ('ULTRA_WIDE', "Ultra-Wide (13mm)", "Ultra-wide lens"),
            ('TELEPHOTO', "Telephoto (65mm)", "Telephoto lens"),
        ],
        default='WIDE',
        update=zoom_update,
    ),
    "iphone_camera_wide_zoom": FloatProperty(
        name="Wide Zoom",
        description="Zoom for wide camera",
        default=26.0,
        min=18.0,
        max=45.0,
        update=zoom_update,
    ),
    "iphone_camera_ultra_wide_zoom": FloatProperty(
        name="Ultra-Wide Zoom",
        description="Zoom for ultra-wide camera",
        default=13.0,
        min=12.0,
        max=18.0,
        update=zoom_update,
    ),
    "iphone_camera_telephoto_zoom": FloatProperty(
        name="Telephoto Zoom",
        description="Zoom for telephoto camera",
        default=65.0,
        min=45.0,
        max=70.0,
        update=zoom_update,
    ),
    "frame_output_directory": StringProperty(
        name="Output Directory",
        description="Directory where the animation frames or video will be stored",
        subtype='DIR_PATH',
        default="//"
    ),
    "animation_output_type": EnumProperty(
        name="Output Type",
        description="Choose whether to render as individual frames or as a video file",
        items=[
            ('FRAMES', "Frames (PNG)", "Render as individual PNG frames"),
            ('AVI', "AVI (JPEG)", "Render as an AVI file with JPEG codec"),
        ],
        default='FRAMES'
    ),
}

class AddCameraScaledUp(Operator):
    bl_idname = "view3d.add_camera_scaled_up"
    bl_label = "Add Scaled Camera"
    
    def execute(self, context):
        # Base name for the camera
        base_name = "Cito_camera"
        suffix = 0
        
        # Check if a camera named "Cito_camera" exists
        cam = bpy.data.objects.get(base_name)
        
        # If it exists, find the next available name (e.g., "Cito_camera_001", "Cito_camera_002", etc.)
        while bpy.data.objects.get(f"{base_name}_{suffix:03}") is not None:
            suffix += 1
        
        # Add a new camera
        bpy.ops.object.camera_add(location=(0, 0, 200))
        cam = bpy.context.active_object
        cam.name = f"{base_name}_{suffix:03}" if suffix > 0 else base_name
        
        # Scale up the camera object (camera objects have no visual geometry, but this scales its icon in the viewport)
        cam.scale = (100, 100, 100)
        
        # Set this new camera as the active camera for the scene
        context.scene.camera = cam
        
        # Change the view to the newly created camera
        bpy.ops.view3d.object_as_camera()
        
        self.report({'INFO'}, f"Camera '{cam.name}' added, scaled, and set as the active view camera.")
    
        return {'FINISHED'}

    
class AddCameraSectionOrtho(Operator):
    bl_idname = "view3d.add_camera_section_ortho"
    bl_label = "Add Section-Ortho Camera"

    def execute(self, context):
        base_name = "Cito_section_camera"
        suffix = 0
        while bpy.data.objects.get(f"{base_name}_{suffix:03}") is not None:
            suffix += 1
        
        # Add a new camera positioned for section view
        bpy.ops.object.camera_add(location=(0, 0, 0))
        cam = bpy.context.active_object
        cam.name = f"{base_name}_{suffix:03}" if suffix > 0 else base_name
        cam.data.type = 'ORTHO'  # Set to orthographic mode
        cam.rotation_euler[0] = 1.5708
        cam.scale = (100, 100, 100)
        cam.data.ortho_scale = 50
        
        context.scene.camera = cam
        bpy.ops.view3d.object_as_camera()

        return {'FINISHED'}
    
class AddCameraTopViewOrtho(bpy.types.Operator):
    bl_idname = "view3d.add_camera_top_view_ortho"
    bl_label = "Add Top-Ortho Camera"

    def execute(self, context):
        base_name = "Cito_top_camera"
        suffix = 0
        while bpy.data.objects.get(f"{base_name}_{suffix:03}") is not None:
            suffix += 1

        bpy.ops.object.camera_add(location=(0, 0, 200))
        cam = bpy.context.active_object
        cam.name = f"{base_name}_{suffix:03}" if suffix > 0 else base_name
        cam.data.type = 'ORTHO'
        cam.scale = (100, 100, 100)
        cam.rotation_euler = (0, 0, 0)  # Top-down view
        cam.data.ortho_scale = 50
        context.scene.camera = cam
        bpy.ops.view3d.object_as_camera()
        
        return {'FINISHED'}

class AddIphoneCamera(bpy.types.Operator):
    bl_idname = "view3d.add_iphone_camera"
    bl_label = "Add iPhone Camera"

    def execute(self, context):
        scene = context.scene
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 5))
        cam = bpy.context.object
        cam.name = "Cito_iPhone_Camera"
        
        # Set lens based on the currently selected zoom mode
        if scene.iphone_camera_zoom_mode == 'WIDE':
            cam.data.lens = scene.iphone_camera_wide_zoom
        elif scene.iphone_camera_zoom_mode == 'ULTRA_WIDE':
            cam.data.lens = scene.iphone_camera_ultra_wide_zoom
        elif scene.iphone_camera_zoom_mode == 'TELEPHOTO':
            cam.data.lens = scene.iphone_camera_telephoto_zoom

        # Set this camera as the active camera
        scene.camera = cam
        return {'FINISHED'}


class ToggleIphoneCameraOrientation(Operator):
    bl_idname = "view3d.toggle_iphone_camera_orientation"
    bl_label = "Toggle Camera Orientation"
    
    def execute(self, context):
        cam = context.scene.camera
        scene = context.scene
        if cam and cam.name.startswith("Cito_"):
            # Toggle orientation based on the custom property
            if cam.get("is_vertical", False):  # Currently in portrait mode
                # Switch to landscape orientation
                cam["is_vertical"] = False
                # Swap resolution to landscape (width > height)
                scene.render.resolution_x, scene.render.resolution_y = scene.render.resolution_y, scene.render.resolution_x
            else:  # Currently in landscape mode
                # Switch to portrait orientation (90 degrees)
                cam["is_vertical"] = True
                # Swap resolution to portrait (height > width)
                scene.render.resolution_x, scene.render.resolution_y = scene.render.resolution_y, scene.render.resolution_x
            
            self.report({'INFO'}, f"Toggled orientation for '{cam.name}' to {'Vertical' if cam['is_vertical'] else 'Horizontal'}")
        else:
            self.report({'WARNING'}, "No active Cito camera found!")
        
        return {'FINISHED'}

class CitoRenderViewport(bpy.types.Operator):
    bl_idname = "view3d.cito_render_viewport"
    bl_label = "Render Viewport Image"
    
    def execute(self, context):
        # Perform a viewport render that matches Blender's Viewport Render Image
        bpy.ops.render.opengl('INVOKE_DEFAULT', view_context=True)
        return {'FINISHED'}

class CitoViewSelectedCamera(bpy.types.Operator):
    bl_idname = "view3d.cito_view_selected_camera"
    bl_label = "View from Selected Camera"
    
    def execute(self, context):
        # Check if the selected object is a camera
        obj = context.object
        if obj and obj.type == 'CAMERA':
            context.scene.camera = obj
            bpy.ops.view3d.object_as_camera()
            self.report({'INFO'}, f"Switched to view from '{obj.name}'")
        else:
            self.report({'WARNING'}, "No camera selected!")
        return {'FINISHED'}

class VIEW3D_OT_CitoCreateAnimationSetup(Operator):
    bl_idname = "view3d.cito_create_animation_setup"
    bl_label = "Create Animation Setup"
    bl_description = "Creates a circular path animation with a camera and an empty target, organized within a single collection"

    def execute(self, context):
        # Define base name for the collection
        base_collection_name = "Cito_Camera_Setup"
        suffix = 1

        # Find a new name for the collection by incrementing the suffix
        while bpy.data.collections.get(f"{base_collection_name}_{suffix:03}"):
            suffix += 1

        # Create the new collection for this animation setup
        collection_name = f"{base_collection_name}_{suffix:03}"
        camera_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(camera_collection)

        # Create an empty object as the camera target and link it to the camera collection
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        target_empty = context.active_object
        target_empty.name = f"Cito_Target_{suffix:03}"
        camera_collection.objects.link(target_empty)

        # Create a circular curve path in the XY plane and link it to the camera collection
        bpy.ops.curve.primitive_bezier_circle_add(radius=100, location=(0, 0, 0))
        path = context.active_object
        path.name = f"Cito_Camera_Path_{suffix:03}"
        path.rotation_euler = (0, 0, 0)  # Ensure path lies in XY plane
        camera_collection.objects.link(path)

        # Add a camera object and link it to the camera collection
        bpy.ops.object.camera_add(location=(0, 0, 0))
        camera = context.active_object
        camera.name = f"Cito_Animated_Camera_{suffix:03}"
        camera_collection.objects.link(camera)

        # Unlink the objects from the scene collection if they are automatically added there
        if target_empty.name in context.scene.collection.objects:
            context.scene.collection.objects.unlink(target_empty)
        if path.name in context.scene.collection.objects:
            context.scene.collection.objects.unlink(path)
        if camera.name in context.scene.collection.objects:
            context.scene.collection.objects.unlink(camera)

        # Add constraints for camera motion
        follow_path = camera.constraints.new(type='FOLLOW_PATH')
        follow_path.target = path
        follow_path.use_curve_follow = True

        track_to = camera.constraints.new(type='TRACK_TO')
        track_to.target = target_empty
        track_to.track_axis = 'TRACK_NEGATIVE_Z'
        track_to.up_axis = 'UP_Y'

        # Set animation properties for the path
        context.scene.frame_start = 1
        context.scene.frame_end = 250
        path.data.path_duration = 250

        # Keyframe the Follow Path constraint's offset factor for a complete loop
        follow_path.offset_factor = 0
        follow_path.keyframe_insert(data_path="offset_factor", frame=context.scene.frame_start)
        follow_path.offset_factor = 1
        follow_path.keyframe_insert(data_path="offset_factor", frame=context.scene.frame_end)

        self.report({'INFO'}, f"Animation setup created: {collection_name}.")
        return {'FINISHED'}


class OBJECT_OT_AnimateFollowPath(Operator):
    bl_idname = "object.animate_follow_path"
    bl_label = "Animate Path"

    def execute(self, context):
        obj = context.active_object
        if obj is None:
            self.report({'ERROR'}, "No active object selected.")
            return {'CANCELLED'}

        follow_path = None
        for constraint in obj.constraints:
            if constraint.type == 'FOLLOW_PATH':
                follow_path = constraint
                break

        if follow_path is None:
            self.report({'ERROR'}, "No 'Follow Path' constraint found.")
            return {'CANCELLED'}
        
        bpy.ops.constraint.followpath_path_animate(constraint=follow_path.name, owner='OBJECT')
        self.report({'INFO'}, "Path animation applied.")
        return {'FINISHED'}
    
class VIEW3D_OT_UseSelectedNURBSToAnimateCamera(Operator):
    bl_idname = "view3d.use_selected_nurbs_to_animate_camera"
    bl_label = "Use Selected NURBS Curve for Camera Animation"
    bl_description = "Assign the selected NURBS curve as the path for the camera, add a target, and animate"

    def execute(self, context):
        # Check if a NURBS curve is selected
        selected_obj = context.active_object
        if selected_obj is None or selected_obj.type != 'CURVE' or not any(spline.type == 'NURBS' for spline in selected_obj.data.splines):
            self.report({'ERROR'}, "Please select a NURBS curve")
            return {'CANCELLED'}
        # Create a unique collection for organizing elements
        collection_name = f"Cito_NURBS_Animation_Setup_{len(bpy.data.collections)}"
        animation_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(animation_collection)

        # Create the camera
        bpy.ops.object.camera_add(location=(0, 0, 0))
        camera = context.active_object
        camera.name = "Cito_Animated_NURBS_Camera"
        animation_collection.objects.link(camera)

        # Unlink the camera from the scene collection
        context.scene.collection.objects.unlink(camera)

        # Add a Follow Path constraint to the camera
        follow_path = camera.constraints.new(type='FOLLOW_PATH')
        follow_path.target = selected_obj
        follow_path.use_curve_follow = True  # This ensures the camera follows the curve orientation
        follow_path.forward_axis = 'FORWARD_X'  # Ensures the camera moves forward (default forward axis for Blender)
        follow_path.up_axis = 'UP_Y'  # Ensures the up axis is Y (Blender default)

        # Create a target in front of the camera, attached to the path
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        target_empty = context.active_object
        target_empty.name = "Cito_Target_NURBS"
        animation_collection.objects.link(target_empty)

        # Attach the target to the same path (optional: offset it slightly forward)
        target_constraint = target_empty.constraints.new(type='FOLLOW_PATH')
        target_constraint.target = selected_obj
        target_constraint.use_curve_follow = True
        target_constraint.offset = -0.1  # Offset target slightly in front of the camera

        # Make the camera track the empty target
        track_to = camera.constraints.new(type='TRACK_TO')
        track_to.target = target_empty
        track_to.track_axis = 'TRACK_NEGATIVE_Z'  # Negative Z-axis (looking forward in Blender cameras)
        track_to.up_axis = 'UP_Y'  # Positive Y-axis as the up axis

        # Set frame range for the animation
        context.scene.frame_start = 1
        context.scene.frame_end = 250
        selected_obj.data.path_duration = 250  # Set the path duration for a smooth loop

        # Keyframe the Follow Path constraint's offset_factor for a complete loop
        follow_path.offset_factor = 0  # Start of the path
        follow_path.keyframe_insert(data_path="offset_factor", frame=context.scene.frame_start)
        
        follow_path.offset_factor = 1  # End of the path (full circle)
        follow_path.keyframe_insert(data_path="offset_factor", frame=context.scene.frame_end)

        self.report({'INFO'}, f"Animation setup created with NURBS path in collection {collection_name}.")
        return {'FINISHED'}

    
class OBJECT_OT_AnimateNURBSPath(Operator):
    """Animate Camera Along NURBS Path"""
    bl_idname = "object.animate_nurbs_path"
    bl_label = "Animate NURBS Path"

    def execute(self, context):
        # Check for the active object
        obj = context.active_object
        if obj is None:
            self.report({'ERROR'}, "No active object selected.")
            return {'CANCELLED'}

        # Find the 'Follow Path' constraint
        follow_path = None
        for constraint in obj.constraints:
            if constraint.type == 'FOLLOW_PATH':
                follow_path = constraint
                break

        if follow_path is None:
            self.report({'ERROR'}, "No 'Follow Path' constraint found.")
            return {'CANCELLED'}
        
        # Run the follow path animation command
        bpy.ops.constraint.followpath_path_animate(constraint=follow_path.name, owner='OBJECT')
        self.report({'INFO'}, "Path animation applied.")
        return {'FINISHED'}

# Operator for Viewport Render Animation with .avi output and JPEG codec
class VIEW3D_OT_CitoViewportRenderAnimation(bpy.types.Operator):
    bl_idname = "view3d.cito_viewport_render_animation"
    bl_label = "Viewport Render Animation"
    bl_description = "Render the viewport animation to the specified output directory"
    
    def execute(self, context):
        scene = context.scene

        # Set the output file path
        scene.render.filepath = bpy.path.abspath(scene.frame_output_directory)
        
        # Check the user's selection for output type
        if scene.animation_output_type == 'FRAMES':
            # Set output format to PNG sequence
            scene.render.image_settings.file_format = 'PNG'
        elif scene.animation_output_type == 'AVI':
            # Set output format to AVI with JPEG codec
            scene.render.image_settings.file_format = 'AVI_JPEG'
        
        # Trigger viewport render animation
        bpy.ops.render.opengl(animation=True, sequencer=False)
        
        self.report({'INFO'}, f"Viewport animation rendering started as {scene.animation_output_type}")
        return {'FINISHED'}


# List of classes operators
classes = [
    AddCameraScaledUp,
    AddCameraSectionOrtho,
    AddCameraTopViewOrtho,
    AddIphoneCamera,
    ToggleIphoneCameraOrientation,
    CitoRenderViewport,
    CitoViewSelectedCamera,
    VIEW3D_OT_CitoCreateAnimationSetup,
    OBJECT_OT_AnimateFollowPath,
    VIEW3D_OT_UseSelectedNURBSToAnimateCamera,
    OBJECT_OT_AnimateNURBSPath,
    VIEW3D_OT_CitoViewportRenderAnimation,
]

def register():
    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)

    # Register properties
    for prop_name, prop_value in properties.items():
        setattr(bpy.types.Scene, prop_name, prop_value)


def unregister():
    # Unregister classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Unregister properties
    for prop_name in properties.keys():
        delattr(bpy.types.Scene, prop_name)
