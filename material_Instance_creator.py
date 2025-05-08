import unreal

# get all selected assets from content browser
def get_selected_content_browser_assets(): 
    editor_utility = unreal.EditorUtilityLibrary()
    selected_assets = editor_utility.get_selected_assets()

    return selected_assets

# generic logging for asset type
def log_asset_types(assets): 
    for asset in assets: 
        unreal.log(f"Asset {asset.get_name()} is a {type(asset)}")

# return any materials in asset list
def find_material_in_assets(assets):
    for asset in assets: 
        
        if type(asset) is unreal.Material: 
            return asset
    return None

# return any texture 2d objects in asset list
def find_textures2D_in_assets(assets): 
    textures = []
    for asset in assets: 
        if type(asset) is unreal.Texture2D: 
            textures.append(asset)
    return textures

def get_random_color(): 
    return unreal.LinearColor(unreal.MathLibrary.rand_range(0,1), unreal.MathLibrary.rand_range(0,1), unreal.MathLibrary.rand_range(0,1))

def create_material_instance(parent_material,asset_path,new_asset_name): 
    
    #create child
    version = 0
    max_versions = 999    
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    material_factory = unreal.MaterialInstanceConstantFactoryNew()
    version_name = f"{new_asset_name}_{version:03}"
    full_path = f"{asset_path}/{version_name}"
    asset_exist = unreal.EditorAssetLibrary.does_asset_exist(full_path)
   
    while version <= max_versions:
        #update versions in core loop to prevent it from checking same thing over and over again
        version_name = f"{new_asset_name}_{version:03}" # the {version:03} transitions the version number into a 3 digit (001,002, 003,etc.)
        full_path = f"{asset_path}/{version_name}"
        asset_exist = unreal.EditorAssetLibrary.does_asset_exist(full_path)

        if asset_exist == True:
            version += 1
            unreal.log("Version already exists, updating")
        else:
            break #should only break when a suitable version is created
    
    if version > max_versions: 
        unreal.log_error("Max versions reached")
        return None
    
    
    new_asset = asset_tools.create_asset(version_name, asset_path,None,material_factory)
    
    #assign parent
    unreal.MaterialEditingLibrary.set_material_instance_parent(new_asset, parent_material)

    return new_asset

def create_mat_inst_for_each (material,textures):
    for texture in textures: 
        unreal.log(f"Creating material instance for texture {texture.get_name()}")
        material_asset_path = unreal.Paths.get_path(texture.get_path_name())
        material_name = f"{material.get_name()}_{texture.get_name()}"

        material_instance = create_material_instance (material,material_asset_path,material_name)

        # Assign texture
        try: 
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(material_instance, "Tex", texture)
        except: 
            unreal.log("Tex parameter does not exist")

        # Assign Color
        try:
            color = get_random_color()
            print (f"Color is {color}")
            unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(material_instance,"Color", color)
        except: 
            unreal.log("Base Color parameter does not exist")
            
        # Save Asset
        unreal.EditorAssetLibrary.save_asset(material_instance.get_path_name(),only_if_is_dirty = True)

# important note: will not work without a texture selected

def run(): 
    unreal.log("Running create material instances script")
    selected_assets = get_selected_content_browser_assets()
    log_asset_types(selected_assets)

    material = find_material_in_assets(selected_assets)
    textures = find_textures2D_in_assets(selected_assets)

    if not material: 
        unreal.log_error("No material selected")
    else: 
        unreal.log(f"Selected material: {material.get_name()}")
    if not textures: 
        unreal.log_error("No texture selected")
    else:     
        unreal.log(f"{len(textures)} textures selected")
    
    create_mat_inst_for_each(material,textures)

run()








