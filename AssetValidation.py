import unreal

## This tool is intended to create an asset validation process that runs through a variety of checks based on the type of asset presented

# get all selected assets in browser
def get_selected_content_browser_assets(): 
    editor_utility = unreal.EditorUtilityLibrary()
    selected_assets = editor_utility.get_selected_assets()

    return selected_assets

# Static Meshes
def staticmesh_validation(asset): 
    
    #variables
    asset_name = asset.get_name()
    max_verts = 5000 #change to user input value once confirmed working
    vert_error_tolerance = 1000
    sm_subsystem = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
    lod_count = sm_subsystem.get_lod_count(asset)
    vert_count = sm_subsystem.get_number_verts(asset,0)
    material_count = sm_subsystem.get_number_materials(asset)
    uv_count = sm_subsystem.get_num_uv_channels(asset,0)
    
    
    if vert_count >= (max_verts+vert_error_tolerance): 
        unreal.log(f"{asset_name} has too many verts, max allowed is {max_verts}")
    else:
        unreal.log(f"{asset_name} vert check passed, moving on")
    if lod_count < 0: 
        unreal.log(f"{asset_name} LOD count shows negative, check log for details")
    else: 
        unreal.log(f"{asset_name} has lods present")
    
    unreal.log (f"{asset_name} contains {material_count} materials, please consult with art guidelines for num materials allowable")
    unreal.log(f"{asset_name} contains {uv_count} uv channels, please consult with art guidelines for appropriate number of uv channels for this asset")

    unreal.log(f"Static Mesh check for {asset_name} complete")

# Materials 
def material_validation(asset):
    unreal.log("loris ipsum")

# Textures 
def texture_validation(asset): 
    size = (asset.blueprint_get_size_x(),asset.blueprint_get_size_y)
    max_size = (2048,2048) #intended to change based on project needs, currently just a selected value

    if size > max_size:  
        unreal.log(f"{asset.get_name()} texture size is too large, please reduce this to {max_size} or less")
    else: 
        unreal.log(f"{asset.get_name()} passes texture checks")

# Niagara 
def niagara_validation(asset):
    unreal.log("loris ipsum") 

# Blueprints
def blueprint_validation(asset):
    unreal.log("loris ipsum") 

# run the script
def run(): 
    selected_assets = get_selected_content_browser_assets()

    for asset in selected_assets:
        unreal.log(f"Begining asset check for {asset.get_name()}") 
        
        if isinstance(asset,unreal.StaticMesh):
            unreal.log(f"{asset.get_name()} is a Static Mesh, beginning Static Mesh checks")
            staticmesh_validation(asset)
        
        #elif isinstance(asset,unreal.BlueprintSystem): 
        #    unreal.log(f"{asset.get_name()} is a Blueprint System, beginning Blueprint System checks")
        #    blueprint_validation()
        
        #elif isinstance(asset,unreal.Niagarasystem): 
        #    unreal.log(f"{asset.get_name()} is a Niagara System, beginning Niagara System checks")
        #    niagara_validation()
        
        elif isinstance(asset,unreal.Material): 
            unreal.log(f"{asset.get_name()} is a Material, beginning Material checks")
            material_validation(asset)
        
        elif isinstance (asset,unreal.Texture):
            unreal.log(f"{asset.get_name()} is a Texture, beginning Texture checks")
            texture_validation(asset)
        
        else: 
            unreal.log("Asset is not on the list of validations") 

run()