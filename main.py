import bpy
from random import random, randint, randrange, uniform
from mathutils import Vector
import bmesh
import math
from bpy import context



bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -1.6))
#bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))


maxIterations = 1000 # Max iterations to prevent while loop from running forever

# min and max values for each axis for the random numbers

num_cubes  = 50 # Number of cubes 
random_loc = []  # Cube coordinates list
random_size = []
spiral_loc = []
spiral_size = []
box_loc = []
sphere_loc = []
#non overlapping // default is consistent sizes // radisu  
def generate_random(random_sizes=False, radius=.25):

    loopIterations = 0
    ranges = {
    'x' : { 'min' : -10, 'max' : 10 },
    'y' : { 'min' : -10, 'max' : 10 },
    'z' : { 'min' : 0, 'max' : 5 }
    }

    # Generates a random number within the axis minmax range
    randLocInRange = lambda axis: ranges[axis]['min'] + random() * ( ranges[axis]['max'] - ranges[axis]['min'] )

    while len( random_loc ) < num_cubes and loopIterations < maxIterations:
        if random_sizes:

            cube_radius  = uniform(.25,5)
        else:
            cube_radius = radius
        
        loopIterations += 1
        print(loopIterations)
        
        # Generate a random 3D coordinate
        loc = Vector([ randLocInRange( axis ) for axis in ranges.keys() ])

        if len( random_loc ) > 0:
            # Search for overlapping points (within the cube radius radius)
            overlappingPoints = [ p for p in random_loc if ( p - loc ).length < cube_radius * 2 ]

            # if any found, skip this location
            if overlappingPoints: continue
        
        # Add coordinate to cube list
        random_loc.append( loc )
        
        random_size.append(cube_radius)

    
def generate_spiral_loc(r,random_sizes=False,radius = .25):
    for i in range(num_cubes):
        if random_sizes:
            cube_radius  = uniform(.25,5)
        else:
            cube_radius = radius
            
        rad = 2 * math.pi * i /12  #Angle calculation 2π i/12
        x = r * math.cos(rad) #x coordinate calculation radius*cosθ
        y = r * math.sin(rad) #y coordinate calculation radius*sinθ
        spiral_loc.append(Vector((x,y,i)))
        spiral_size.append(cube_radius)


def generate_sphere_loc():
    x_center = 0.0
    y_center = 0.0
    z_center = 0.0
    scale = 8.0

    # Baseline size of each cube.
    sz_max = math.sqrt(2.0) * 6.0 / scale
    sz_min = sz_max / 16.0

    latitude = 16
    longitude = latitude * 2

    inv_latitude = 1.0 / (latitude - 1)
    inv_longitude = 1.0 / (longitude - 1)

    gamma = 1

    lat_lon = latitude * longitude
    grid_range = range(0, lat_lon, 1)
    for n in grid_range:
        i = n // longitude
        j = n % longitude

        i_prc = i * inv_latitude
        inclination = math.pi * (i + 1) * inv_latitude
        sin_incl = math.sin(inclination)
        cos_incl = math.cos(inclination)

        # Back-slash \ allows long lines to be
        # wrapped to new line without an error.
        incl_fac = abs(sin_incl)
        sz_cube = (1.0 - incl_fac) * sz_min \
            + incl_fac * sz_max

        # TWOPI from the random module
        # can be replaced with tau from math.
        j_prc = j * inv_longitude
        azimuth = math.tau * j / longitude
        sin_azim = math.sin(azimuth)
        cos_azim = math.cos(azimuth)

        # Spherical to Cartesian conversion.
        x = sin_incl * cos_azim * scale
        y = sin_incl * sin_azim * scale
        z = cos_incl * scale   
        sphere_loc.append(Vector((x,y,z)))

#def generate_random_materials_(
def generate_box_loc():  
    # Number of cubes on each axis.
    count = 2

    # Range used with for-loops.
    count_range = range(0, count, 1)

    # Size of grid.
    extents = 2.0

    # To convert abstract grid position within loop to real-world coordinate.
    inv_count = 1.0 / (count - 1.0)
    diff = extents + extents

    # Spacing between cubes.
    padding = 0.5

    # Size of each cube.
    sz_cube = (diff / count) - padding

    # Center of grid.
    z_center = 0.0
    y_center = 0.0
    x_center = 0.0

    # Loop through grid z axis.
    for i in count_range:

        # Convert from index to percent in range [0.0, 1.0],
        # then convert from prc to real world coordinate.
        # Equivalent to map(val, lb0, ub0, lb1, ub1).
        i_prc = i * inv_count
        z = -extents + i_prc * diff
        z = z + z_center
        blue = i_prc

        # Loop through grid y axis.
        for j in count_range:
            j_prc = j * inv_count
            y = -extents + j_prc * diff
            y = y + y_center
            green = j_prc

            # Loop through grid x axis.
            for k in count_range:
                k_prc = k * inv_count
                x = -extents + k_prc * diff
                x = x + x_center
                red = k_prc

                # Combine x, y and z into a tuple.
                box_loc.append(Vector((x,y,z)))
 
    

def clear_collection ():
    remove_collection_objects = True

    coll = context.collection
    scene = context.scene

    if coll:
        if remove_collection_objects:
            obs = [o for o in coll.objects if o.users == 1]
            while obs:
                bpy.data.objects.remove(obs.pop())

        if coll is not scene.collection:
            bpy.data.collections.remove(coll)

def random_vectors(bm, delta = .2):
    for v in bm.verts:
        if not v.select:
            continue
        v.co.xy += Vector([uniform(-delta, delta) for axis in "xy"])

def random_colors(me, count=6):
    for i in range(count):
        mat = bpy.data.materials.new("Mat_%i" % i)
        mat.diffuse_color = random(), random(), random(), 1
        me.materials.append(mat)
   # All the materials of the selected object
    no_of_materials = len(me.materials)
    for face in bm.faces:
        face.material_index = randint(0, no_of_materials - 1)  # Assing random material to face

def color_theme_1(me):
    x = random()
    print(x)
    print(type(random))
    mat = bpy.data.materials.new("a")
    mat.diffuse_color = 206/255, 235/255, 251/255, 1
    me.materials.append(mat)

    mat2 = bpy.data.materials.new("b")
    mat2.diffuse_color = 163/255, 214/255, 245/255, 1
    me.materials.append(mat2)

    mat3 = bpy.data.materials.new("c")
    mat3.diffuse_color = 102/255,167/255,197/255,1
    me.materials.append(mat3)

    mat4 = bpy.data.materials.new("d")
    mat4.diffuse_color = 238/255,50/255,51/255,1
    me.materials.append(mat4)

    mat5 = bpy.data.materials.new("e")
    mat5.diffuse_color = 240/255,236/255,235/255,1
    me.materials.append(mat5)

    mat6 = bpy.data.materials.new("f")
    mat6.diffuse_color = 108/255,116/255,118/255,1
    me.materials.append(mat6)



    no_of_materials = len(me.materials)
    for face in bm.faces:
        face.material_index = randint(0, no_of_materials - 1)  # Assing random material to face



generate_random()
generate_spiral_loc(5, radius=1)
generate_box_loc()
generate_sphere_loc()
clear_collection()


for i in range(len(box_loc)):
    bpy.ops.mesh.primitive_cube_add(size=1, location = box_loc[i])
    bpy.ops.object.mode_set(mode='EDIT')
    #bpy.ops.mesh.subdivide(number_cuts=3)
    obj = bpy.context.object
    r=uniform(3,6.2)
    bpy.ops.transform.rotate(value=r, orient_axis = 'Y')

    me = obj.data
    bm = bmesh.from_edit_mesh(me) 
    color_theme_1(me)
    

    
    
   
   
    #random_vectors(bm)
    bpy.ops.object.mode_set(mode='OBJECT')
    #modifier = obj.modifiers.new(name="Geom", type='GeometryNodes')

    

   
    


# item='MESH'
# bpy.ops.object.select_all(action='DESELECT')
# bpy.ops.object.select_by_type(type=item)
# bpy.ops.object.join()  
# obj = bpy.context.object

# for i in range (len(spiral_loc)):
#    new = bpy.data.objects.new(str(i) + " cube", obj.data)
#    new.location = spiral_loc[i]
#    context.collection.objects.link(new)

    
        
        
    
