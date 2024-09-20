import unreal as ue

def get_selected_content_browser_assets(): 
    editor_utility = ue.EditorUtilityLibrary()
    selected_assets = editor_utility.get_selected_assets()

    return selected_assets

def return_new_name(asset): 
    name = asset.get_name()
    if isinstance(asset,ue.MaterialInstance) and not name.startswith("MI_"): 
        return "MI_" + asset.get_name() 
    elif isinstance(asset, ue.Material) and not name.startswith("M_"): 
        return "M_" + asset.get_name()
    elif isinstance (asset, ue.Texture) and not name.startswith("T_"): 
        return "T_" + (asset, ue.Texture)
    elif isinstance (asset,ue.NiagaraSystem) and not name.startswith("NS_"): 
        return "NS_" + asset.get_name()
    elif isinstance(asset,ue.StaticMesh) and not name.startswith("SM_"): 
        return "SM_"+ asset.get_name()

def run ():
    selected_assets = get_selected_content_browser_assets()
    print (selected_assets)
    for asset in selected_assets:
        old_name = asset.get_name()
        old_path = asset.get_path_name()
        asset_folder = ue.Paths.get_path(old_path)

        new_name = return_new_name(asset)
        new_path = asset_folder + '/' + new_name
        if new_name == old_name: 
            print (f"Ignoring {old_name}, it is already correct")
            continue
        rename_success = ue.EditorAssetLibrary.rename_asset(old_path, new_path)
        if not rename_success: 
            ue.log_error("Could not rename: " + old_path)


    

run()