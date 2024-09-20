'''
Place cubes in a circle
'''
import unreal
import math

def spawn_cube (location = unreal.Vector(),rotation = []):
    # get system to control actors
    editor_actor_subs = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    # create StaticMeshActor
    actor_class = unreal.StaticMeshActor

    # place in level - takes the location and rotation params fed in
    static_mesh_actor = editor_actor_subs.spawn_actor_from_class(actor_class, location,rotation)
    
    # load and add cube
    static_mesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube.cube")
    static_mesh_actor.static_mesh_component.set_static_mesh(static_mesh)


def run(): 
    
    cube_count = 60
    for i in range (cube_count): 
        
        '''
        This was a silly way to try to do this. the pi(r^2) approach just sets the y value at that value, not in a circle. C'mon. 
        pi = math.pi
        r = 1000
        

        circle_x_location = i * 150
        circle_y_location = pi*(r**2)
        '''

        cube_count = 30
        circle_radius = 2000
        circle_center = unreal.Vector(0,0,0)

        for i in range(cube_count): 
            circle_x_location = circle_radius * math.cos(math.radians(i * 360/cube_count))
            circle_y_location = circle_radius * math.sin(math.radians(i * 360/cube_count))        
            location = unreal.Vector(circle_x_location,circle_y_location,0)
            # rotation. Reminder: Vector has a quaternion fucntion in it. 
            location_to_circle_center = location - circle_center
            rotation = location_to_circle_center.quaternion().rotator()
            
            spawn_cube(location,rotation)

            
# Unreal considers each placed cube an action and saves the operations as they occur. To avoid this and be able to undo all at once, use this as the run method: 
with unreal.ScopedEditorTransaction("Place cubes in a circle") as trans: 
    run()