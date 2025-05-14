import unreal as ue
import math

#Spawn a cube with a set location and rotation
def spawnCube(location = ue.Vector(), rotation = ue.Rotator()): 

    #this gets the subsystem that controls actors in the editor
    editor_actor_subs = ue.get_editor_subsystem(ue.EditorActorSubsystem)

    #set actor to a static mesh
    actor_class = ue.StaticMeshActor

    #spawn in level
    static_mesh_actor = editor_actor_subs.spawn_actor_from_class(actor_class,location, rotation)

    #load and add cube. Dir path is truncated in UE, so you don't have to have the full path, 
    # just the /Engine/Folder/object.objtype path, see below

    static_mesh = ue.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube.Cube")
    static_mesh_actor.static_mesh_component.set_static_mesh(static_mesh)
# could maybe shorten this to
# static_mesh_actor.static_mesh_component.set_static_mesh(unreal.EditorAssetLIbrary.load_asset("/Engine/BasicShapes/Cube.Cube"))
# Unsure though, worth trying. 

def run(numCubes, radius,center): 

    count = numCubes
    r = 1000
    c = center

    for i in range(count): 
        
        # x multiplies the circle radius by cosine with i * degrees over number of cubes to spawn
        circlex = r * math.cos(math.radians(i*360/count))
        # y multiplies radius by sine then the same
        circley = r*math.sin(math.radians(i*360/count))

        location = ue.Vector(circlex,circley,1000)
        #get the length between the location of the cube and the center of the circle
        centerloc = location - c
        #rotate the cube to face the center of the circle
        rotation = centerloc.quaternion().rotator()
        spawnCube(location,rotation)

with ue.ScopedEditorTransaction("Place cubes in a circle") as trans:
    run(30,1000, ue.Vector(0,0,0))