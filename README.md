# Blender 3D addon : Merge Selected Vertices

## Overview
The Merge Selected Vertices addon enables you to merge selected vertices within Blender. It provides options to specify the axis and direction for merging the vertices.

## Installation
1. Download the addon zip file from [here](https://github.com/drekorig/MeshMergeSelectedVertices/archive/refs/heads/main.zip).
2. Launch Blender and navigate to `Edit` > `Preferences`.
3. Go to the `Add-ons` tab.
4. Click the `Install...` button and select the downloaded zip file.
5. Enable the addon by ticking the checkbox next to its name.

## Usage
- Open Blender and switch to Edit Mode.
- Select the vertex you wish to merge.
- Go to `Mesh` > `Merge` > `By Selection` in the menu bar.
- Alternatively, you can press 'M' in Edit Mode and select 'By Selection'.
- In the options panel, specify the desired axis and direction for merging the vertices.
- Click the `Merge` button to execute the merge operation.

## Options
- **Axis:** Select the axis (X, Y, or Z) along which the vertices will be merged.
- **Threshold:** Define the merge distance from the selected vertex.
- **Inverse Direction:** Toggle to reverse the merge direction.

## Notes
- At least one vertex must be selected for the merge operation to be performed.
- Ensure the merge threshold is suitable for your mesh to prevent unintentional merging of distant vertices.
