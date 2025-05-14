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

# Blueprints
def blueprint_validation(asset):
    asset_name = asset.get_name()
    library = unreal.EditorAssetLibrary
    blueprints = library.load_asset(asset.get_)    
    generated_class = blueprints.generated_class
    cdo = generated_class.get_default_object()
    components = cdo.get_components_by_class(unreal.ActorComponent)
    num_components = len(components)
    max_components = 20

    unreal.log (f"{asset_name} is of class {generated_class}")

    if num_components > max_components: 
        unreal.log(f"{asset_name} has more than the max components of {max_components}, please reduce the number of components used")
    else: 
        unreal.log(f"{asset_name} passes blueprint checks")

# Niagara 
def niagara_validation(asset):
    asset_name = asset.get_name()
    niagara_system = unreal.NiagaraComponent(asset)
    fixed_bounds = niagara_system.get_system_fixed_bounds()
    perf_baseline = niagara_system.init_for_performance_baseline()

    unreal.log(f"The fixed bounds for {asset_name} are {fixed_bounds}")
    unreal.log(f"Running perf baseline: {perf_baseline}")

# Materials 
def material_validation(asset):
    asset_name = asset.get_name()
    material_library = unreal.MaterialEditingLibrary
    material_expressions = material_library.get_num_material_expressions(asset)
    scalar_params = material_library.get_scalar_parameter_names(asset)
    static_switch_params = material_library.get_static_switch_parameter_names(asset)
    get_stats = material_library.get_statistics(asset)
    texture_params = material_library.get_texture_parameter_names(asset)
    textures_used = material_library.get_used_textures(asset)
    vector_params = material_library.get_vector_parameter_names (asset)

    unreal.log(f"{asset_name} has the following attributes: ")
    unreal.log("------------------------------------------------------")
    unreal.log("General Material Statistics")
    unreal.log(f"Number of Samplers: {get_stats.num_samplers}")
    unreal.log(f"Number of Pixel Shader Instructions: {get_stats.num_pixel_shader_instructions}")
    unreal.log(f"Number of Vertex Shader Instructions: {get_stats.num_vertex_shader_instructions}")   
    unreal.log(f"Number of UV Scalars: {get_stats.num_uv_scalars}")
    unreal.log("------------------------------------------------------")
    unreal.log("Number of Material Expressions")
    unreal.log(f"{material_expressions}")
    unreal.log("------------------------------------------------------")
    unreal.log("List of Scalar Parameters")
    for i in scalar_params:
        unreal.log(f"{i}")
    unreal.log("------------------------------------------------------")
    unreal.log("List of Vector Parameters")
    for i in vector_params:
        unreal.log(f"{i}")
    unreal.log("------------------------------------------------------")
    unreal.log("List of Texture Parameters")
    for i in texture_params:
        unreal.log(f"{i}")
    unreal.log("------------------------------------------------------")
    unreal.log("List of Textures Used")
    for i in textures_used:
        unreal.log(f"{i}")
    unreal.log("------------------------------------------------------")
    unreal.log("List of Static Switch Parameters")
    for i in static_switch_params:
        unreal.log(f"{i}")
    unreal.log("------------------------------------------------------")
    unreal.log(f"{asset_name} material validation checks complete")
    
    
# Textures 
def texture_validation(asset): 
    size = (asset.blueprint_get_size_x(),asset.blueprint_get_size_y)
    max_size = (2048,2048) #intended to change based on project needs, currently just a selected value

    if size > max_size:  
        unreal.log(f"{asset.get_name()} texture size is too large, please reduce this to {max_size} or less")
    else: 
        unreal.log(f"{asset.get_name()} passes texture checks")

# run the script
def run(): 
    selected_assets = get_selected_content_browser_assets()

    for asset in selected_assets:
        unreal.log(f"Begining asset check for {asset.get_name()}") 
        
        if isinstance(asset,unreal.StaticMesh):
            unreal.log(f"{asset.get_name()} is a Static Mesh, beginning Static Mesh checks")
            staticmesh_validation(asset)
        
        elif isinstance(asset,unreal.Blueprint): 
            unreal.log(f"{asset.get_name()} is a Blueprint System, beginning Blueprint System checks")
            blueprint_validation(asset)
        
        elif isinstance(asset,unreal.NiagaraSystem): 
            unreal.log(f"{asset.get_name()} is a Niagara System, beginning Niagara System checks")
            niagara_validation(asset)
        
        elif isinstance(asset,unreal.Material): 
            unreal.log(f"{asset.get_name()} is a Material, beginning Material checks")
            material_validation(asset)
        
        elif isinstance (asset,unreal.Texture):
            unreal.log(f"{asset.get_name()} is a Texture, beginning Texture checks")
            texture_validation(asset)
        
        else: 
            unreal.log("Asset is not on the list of validations")
            

run()