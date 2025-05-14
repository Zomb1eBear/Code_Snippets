import unreal


# get all selected browser assets
# IMPORTANT: calling the function EditorUtilityLibrary from unreal has been deprecated in 5.5
# To get around this, what I have done is call the Editor Utility Library function as a from unreal import
# this seems to work correctly, though i still get a deprecation warning. 

def get_selected_content_browser_assets(): 
    editor_utility = unreal.EditorUtilityLibrary()
    selected_assets = editor_utility.get_selected_assets()

    return selected_assets

# This way is technically correct and accurate, however it is slightly less easy to modify later
# down the road. The newer version allows for a config for easy updating. Otherwise the functionaltiy 
# is the same

#def name_change(asset): 
    #name = asset.get_name()

    #inheritance is important. Material Instance inherits from Material, so MUST be checked first
    # if isinstance(asset,unreal.MaterialInstance) and not name.startswith("MI_"):
    #    return "MI_" + asset.get_name()
    # elif isinstance(asset,unreal.Material) and not name.startswith("M_"):
    #   return "M_" + asset.get_name()
    # elif isinstance(asset,unreal.Texture) and not name.startswith("T_"):
    #    return "T_" + asset.get_name()
    # elif isinstance(asset,unreal.NiagaraSystem) and not name.startswith("NS_"):
    #     return "NS_" + asset.get_name()
    # elif isinstance(asset,unreal.StaticMesh) and not name.startswith("SM_"):
    #    return "SM_" + asset.get_name()
    # else: 
    #     return asset.get_name()

def name_change(asset): 
    rename_config = {
            "prefixes_per_type": [
            {"type": unreal.MaterialInstance, "prefix": "MI_"},
            {"type": unreal.Material, "prefix": "M_"},
            {"type": unreal.Texture, "prefix": "T_"},
            {"type": unreal.NiagaraSystem, "prefix": "NS_"},
            {"type": unreal.StaticMesh, "prefix": "SM_"},
            {"type": unreal.ParticleSystem, "prefix": "C_"}
        ]
    }
    
    name = asset.get_name()

    print (f"Asset {name} is a {type(asset)}")

    for i in range(len(rename_config["prefixes_per_type"])):
        prefix_config = rename_config["prefixes_per_type"][i]

        prefix = prefix_config["prefix"]
        asset_type = prefix_config["type"]

        if isinstance(asset,asset_type) and not name.startswith(prefix): 
            return prefix + name
    

def rename_assets(assets): 
    for i in assets: 
        asset = i
        
        # get the old name, path, and folder information for asset
        old_name = asset.get_name()
        asset_old_path = asset.get_path_name()
        asset_folder =  unreal.Paths.get_path(asset_old_path)

        # set new name and path 
        new_name = name_change(asset)
        new_path = f"{asset_folder}/{new_name}"
        print (f"{old_name} -> {new_name}")

        rename_success = unreal.EditorAssetLibrary.rename_asset(asset_old_path,new_path)
        if not rename_success: 
            unreal.log_error("Could not rename: " + asset_old_path)

def run(): 
    selected_assets = get_selected_content_browser_assets()
    rename_assets(selected_assets)




# it appears super important to have a run function for major functionatliy in python in UE. 
# I think it may be because the "run" functionality in UE is looking for a "run" function in the python
# script. So use this knowledge going forward. 

run()
