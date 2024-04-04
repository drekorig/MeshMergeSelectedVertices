bl_info = {
    "name": "Merge Selected Vertices",
    "author": "Drekorig",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "category": "Mesh Editing",
    "location": "Mesh > Merge Selected",
    "description": "Addon for merging vertices in mesh editing.",
    "warning": "",
    "doc_url": "https://github.com/drekorig/MeshMergeSelectedVertices",
}

from .addon import MeshMergeSelectedVertices

# Plugin registration


def merge_vertices_button(self, context):
    """Add merge vertices button"""
    self.layout.operator(
        MeshMergeSelectedVertices.bl_idname,
        text="By Selection")


def merge_vertices_manual_map():
    """This allows you to right click on a button and link to documentation"""
    url_manual_prefix = "https://github.com/drekorig/MeshMergeSelectedVertices/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "blob/main/README.md"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    """Register addon"""
    bpy.utils.register_class(MeshMergeSelectedVertices)
    bpy.utils.register_manual_map(merge_vertices_manual_map)
    bpy.types.VIEW3D_MT_edit_mesh_merge.append(merge_vertices_button)


def unregister():
    """Unregister addon"""
    bpy.utils.unregister_class(MeshMergeSelectedVertices)
    bpy.utils.unregister_manual_map(merge_vertices_manual_map)
    bpy.types.VIEW3D_MT_edit_mesh_merge.remove(merge_vertices_button)


if __name__ == "__main__":
    register()
