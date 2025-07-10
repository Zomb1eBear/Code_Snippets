import unreal as ue

#Unreal Params
world = ue.EditorLevelLibrary.get_editor_world()
editor_lev = ue.EditorLevelLibrary()

#Actors
selected_actors = editor_lev.get_selected_level_actors()
#This sets the object types that are referenced by the line trace. If the object type is of the types specified, it will return True
obj_types = [ue.ObjectTypeQuery.OBJECT_TYPE_QUERY1, ue.ObjectTypeQuery.OBJECT_TYPE_QUERY2]

#Vector info
start = ue.Vector(0,0,100)
end = ue.Vector(0,0,0)

for actor in selected_actors:
    #set transform to actor transform then get the location
    location = actor.get_actor_location()
    start = location
    end = ue.Vector(0,0,location.z - 1000)
    #start = transform.translation()
    #end = transform.translation()-(0,0,100)

    #print(start)
    #print(end)
    hit = ue.SystemLibrary.line_trace_single_for_objects(
        world_context_object = world,
        start = start,
        end = end,
        object_types = obj_types,
        trace_complex = True, 
        actors_to_ignore=[],
        draw_debug_type = ue.DrawDebugTrace.FOR_ONE_FRAME,
        trace_color = ue.LinearColor.RED,
        trace_hit_color = ue.LinearColor.BLUE,
        draw_time = 5.0
    )


    if hit:
        outhit=hit.to_tuple()
        impact = outhit[5]
        distance = start.z - impact.z
        actor_move = ue.Vector(start.x,start.y,start.z-distance)

        print(actor_move)

        if abs(distance) > 10:
            actor.set_actor_location_and_rotation(actor_move,actor.get_actor_rotation(),True,True)
        