import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.Geometry as rg
import Rhino.DocObjects as rd
import math

def voxelize_brep(brep, z , points_guid):
    bbox = rs.BoundingBox(brep)
    if bbox is None:  # Check if bounding box exists
        return None

    min_pt, max_pt = bbox[0], bbox[6]
    x_span = max_pt.X - min_pt.X
    y_span = max_pt.Y - min_pt.Y
    z_span = max_pt.Z - min_pt.Z

    x_voxels = int(x_span / voxel_size) + 1
    y_voxels = int(y_span / voxel_size) + 1
    z_voxels = int(z_span / voxel_size) + 1

    voxels = []

    for i in range(x_voxels):
        for j in range(y_voxels):
            for k in range(z_voxels):
                x = min_pt.X + i * voxel_size
                y = min_pt.Y + j * voxel_size
                z = min_pt.Z + k * voxel_size
                voxel = rg.Box(rg.Plane.WorldXY, rg.Interval(x, x + voxel_size), rg.Interval(y, y + voxel_size), rg.Interval(z, z + voxel_size))
                voxel_guid = sc.doc.Objects.AddBrep(voxel.ToBrep())
                intersect = rg.Intersect.Intersection.BrepBrep(brep, voxel.ToBrep(), sc.doc.ModelAbsoluteTolerance)
                voxel_brep = voxel.ToBrep()
                
                #calculate the closest point in the to the voxel
                voxel_centroid = rg.AreaMassProperties.Compute(voxel_brep).Centroid
                #closest_point = brep.ClosestPoint(rs.coercebrep(brep_guid))
                coordinates = []
                
                for point in points_guid:
                    coordinates.append(rs.PointCoordinates(point))
                #use that infor to extract the info of the point to get the color
                closest_point, point_index = find_closest_point(voxel_centroid, coordinates)
                point_property = get_point_property(points_guid[point_index])
                
                if len(intersect[1]) > 0:
                    rs.ObjectColor(voxel_guid, point_property)
                    voxels.append(voxel_guid)
                else: 
                    rs.DeleteObject(voxel_guid)

    return voxels

def get_point_property(point):
    
    #If ColorSource is ON::color_from_object, then value of m_color is used.
    color = rs.ObjectColor(point)
    return color
    
def find_closest_point(target_point, point_set):
    closest_point = None
    closest_point_index = None
    min_distance = float('inf')

    for i in range(len(point_set)):
        distance = target_point.DistanceTo(point_set[i])
        if distance < min_distance:
            min_distance = distance
            closest_point = point_set[i]
            closest_point_index = i

    return closest_point, closest_point_index
    
brep_guid = rs.GetObject("Select a Brep", rs.filter.surface | rs.filter.polysurface)
points_guid = rs.GetObjects("Select points", rs.filter.point)


#points = [rs.coerce3dpoint(points_guid) for point_guid in point_guids]


voxel_size = rs.GetReal("Enter voxel size", 2.0)
voxels = voxelize_brep(rs.coercebrep(brep_guid), voxel_size, points_guid)
