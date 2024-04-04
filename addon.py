import bmesh
import bpy
from mathutils import Vector
from bpy.props import FloatVectorProperty
from bpy.types import Operator


class MeshMergeSelectedVertices(Operator):
    """Merge Selected Vertices"""
    bl_idname = "mesh.merge_vertex"
    bl_label = "Merge Vertices"
    bl_options = {'REGISTER', 'UNDO'}

    # Properties
    axis_items = [
        ('X', 'X', "X Axis", 'XAXIS', 0),
        ('Y', 'Y', "Y Axis", 'YAXIS', 1),
        ('Z', 'Z', "Z Axis", 'ZAXIS', 2),
    ]

    # Axis choice
    merge_axis: bpy.props.EnumProperty(
        name="Axis",
        description="Axis to merge on",
        items=axis_items,
        default=0,
    )
    # Threshold for merging
    threshold: bpy.props.FloatProperty(
        name="Threshold",
        description="Merge distance from a selected vertex",
        default=0.001,
    )

    # Direction inverse
    inverse_direction: bpy.props.BoolProperty(
        name="Inverse Direction",
        description="Inverse the merge direction",
        default=False
    )

    # Execute function
    def execute(self, context):
        """Merge vertices"""
        # Merge vertices
        result = self.merge_selected()
        return result

    def merge_selected(self):
        """Merge selected vertices"""
        # Initialize variables
        adjacent_vert_not_found = False
        # Axis list
        axis_enum = {'X': 0, 'Y': 1, 'Z': 2}
        axis = [0, 1, 2]
        index_axis = axis_enum[self.merge_axis]
        # Remove merge axis
        axis.remove(index_axis)
        # Get merge direction
        direction = not self.inverse_direction
        # Get the active object (assuming it's a mesh)
        obj = bpy.context.active_object

        # Check if object is in Edit Mode
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Object is not in Edit Mode.")
            return {'CANCELLED'}
        # Get the mesh from edit mode
        bm = bmesh.from_edit_mesh(obj.data)

        # Get all selected vertices
        selected_verts = [v for v in bm.verts if v.select]
        # Check if at least one vertex is selected
        if not selected_verts:
            self.report({'WARNING'}, "At least one vertex must be selected.")
            return {'CANCELLED'}

        for selected_vert in selected_verts:
            # Get adjacent vertex
            adjacent_vert = None
            # Get edge length
            adjacent_edge_length = None

            # Loop through connected edges
            for edge in selected_vert.link_edges:
                edge_length = edge.calc_length()
                # Get the other vertex on the edge
                other_vert = edge.other_vert(selected_vert)
                if not other_vert or other_vert in selected_verts:
                    continue
                # Check if other vertex in selected direction
                if direction:
                    if selected_vert.co[index_axis] > other_vert.co[index_axis]:
                        continue
                else:
                    if selected_vert.co[index_axis] < other_vert.co[index_axis]:
                        continue
                # Check if other vertex is close to selected vertex
                if abs(selected_vert.co[axis[0]] - other_vert.co[axis[0]]) < self.threshold and abs(
                        selected_vert.co[axis[1]] - other_vert.co[axis[1]]) < self.threshold:
                    # Check if adjacent vertex already exists
                    if not adjacent_vert:
                        adjacent_vert = other_vert
                        adjacent_edge_length = edge_length
                        continue
                    if adjacent_edge_length > edge_length:
                        adjacent_vert = other_vert
                        adjacent_edge_length = edge_length

            self.report({'DEBUG'}, f"Point selected {selected_vert.index}: {selected_vert.co}")
            if adjacent_vert:
                self.report({'DEBUG'}, f"Point adjacent {adjacent_vert.index}: {adjacent_vert.co}")

                # Select adjacent vertex
                adjacent_vert.select = True
                # Calculate middle point
                middle_point = (selected_vert.co + adjacent_vert.co) / 2
                # Set middle point to selected vertex
                selected_vert.co = adjacent_vert.co = middle_point
            else:
                self.report({'DEBUG'}, "No adjacent vertex found.")
                adjacent_vert_not_found = True

        # Merge selected vertex with adjacent vertex
        bpy.ops.mesh.remove_doubles(threshold=0.0)
        if adjacent_vert_not_found:
            self.report({'INFO'}, "Some vertices could not be merged. No adjacent vertex found.")
        else:
            self.report({'INFO'}, "Merge operation performed successfully.")
        return {'FINISHED'}
