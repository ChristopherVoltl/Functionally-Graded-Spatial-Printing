import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.Geometry as rg
import Rhino.DocObjects as rd
import math
import os
import System
import System.Collections.Generic
import Rhino

def SampleViewCaptureToFile(name):
    view = sc.doc.Views.ActiveView;
    if view:
        view_capture = Rhino.Display.ViewCapture()
        view_capture.Width = view.ActiveViewport.Size.Width
        view_capture.Height = view.ActiveViewport.Size.Height
        view_capture.ScaleScreenItems = False
        view_capture.DrawAxes = False
        view_capture.DrawGrid = False
        view_capture.DrawGridAxes = False
        view_capture.TransparentBackground = True
        bitmap = view_capture.CaptureToBitmap(view)
        if bitmap:
            bitmap.Save(name, System.Drawing.Imaging.ImageFormat.Png);



def voxelize_brep(brep, voxel_size, points_guid):
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
    color = []
    voxel_guids = []
    renderCount = 1

    for i in range(x_voxels):
        for j in range(y_voxels):
            for k in range(z_voxels):
                x = min_pt.X + i * voxel_size
                y = min_pt.Y + j * voxel_size
                z = min_pt.Z + k * voxel_size
                voxel = rg.Box(rg.Plane.WorldXY, rg.Interval(x, x + voxel_size), rg.Interval(y, y + voxel_size), rg.Interval(z, z + voxel_size))
                voxel_guid = sc.doc.Objects.AddBrep(voxel.ToBrep())
                voxel_guids.append(voxel_guid)
                intersect = rg.Intersect.Intersection.BrepBrep(brep, voxel.ToBrep(), sc.doc.ModelAbsoluteTolerance)
                voxel_brep = voxel.ToBrep()
                
                #calculate the closest point in the to the voxel
                voxel_centroid = rg.AreaMassProperties.Compute(voxel_brep).Centroid
                #closest_point = brep.ClosestPoint(rs.coercebrep(brep_guid))
                coordinates = []
                
                for point in points_guid:
                    coordinates.append(rs.PointCoordinates(point))
                #use that info to extract the info of the point to get the color
                closest_point, point_index = find_closest_point(voxel_centroid, coordinates)
                point_property = get_point_property(points_guid[point_index])

                voxelCorners = voxel.GetCorners()
                
                #TEST INSIDE BREP ONLY IF THE 8 CORNER POINTS ARE INSIDE THE BREP ******new****
                cornerCount = 0
                for corner in voxelCorners:
                    isPointonSrf = is_point_on_brep(corner, brep)
                    if rg.Brep.IsPointInside(brep, corner, sc.doc.ModelAbsoluteTolerance, True) or isPointonSrf is True:
                        cornerCount+=1
                if cornerCount == 8:
                    rs.ObjectColor(voxel_guid, point_property)
                    voxels.append(voxel)
                    color.append([point_property.R, point_property.G, point_property.B])
                else:
                    print("The point is not inside the Brep.")
                    rs.DeleteObject(voxel_guid)
                
                cornerCount = 0
                '''
                if len(intersect[1]) > 0:
                    rs.ObjectColor(voxel_guid, point_property)
                    voxels.append(voxel)
                    color.append([point_property.R, point_property.G, point_property.B])

                    location = "C:/Users/Chris/Desktop/Temp/Voxel/"
                    name = location + "Voxel" + "000" + str(renderCount) + ".png"
                    SampleViewCaptureToFile(name)
                    renderCount = renderCount + 1
                else: 
                    #test inside or outside ****old*****
                    if rg.Brep.IsPointInside(brep, voxel_centroid, sc.doc.ModelAbsoluteTolerance, True):
                        print("The point is inside the Brep.")
                        rs.ObjectColor(voxel_guid, point_property)
                        voxels.append(voxel)
                        color.append([point_property.R, point_property.G, point_property.B])
                    else:
                        print("The point is not inside the Brep.")
                        rs.DeleteObject(voxel_guid)
                        '''


    return voxels, color, voxel_guids

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
    


def toolpath_to_voxel(voxels, color, highdensity, hd_centroid, meddensity, md_centroid, lowdensity, ld_centroid):
    
    for voxel in range(len(voxels)):
      #voxel_guid = sc.doc.Objects.AddBrep(voxels[voxel].ToBrep())
      color[voxel]
      voxel_brep = voxels[voxel].ToBrep()
      print(color[voxel])
      if color[voxel][0] == 255 and color[voxel][1] == 0:
          print("meow")
          voxel_centroid = rg.AreaMassProperties.Compute(voxel_brep).Centroid
          start_point = rs.coerce3dpoint(hd_centroid)
          end_point = rs.coerce3dpoint(voxel_centroid)
          
          vector = rg.Vector3d(end_point - start_point)
          rs.CopyObject(highdensity, vector)
      elif color[voxel][0] == 255 and color[voxel][1] == 255:
          print("moo")
          voxel_centroid = rg.AreaMassProperties.Compute(voxel_brep).Centroid
          start_point = rs.coerce3dpoint(md_centroid)
          end_point = rs.coerce3dpoint(voxel_centroid)
          
          vector = rg.Vector3d(end_point - start_point)
          
          rs.CopyObject(meddensity, vector)
      elif color[voxel][0] == 0 and color[voxel][1] == 255:
          print("woof")
          voxel_centroid = rg.AreaMassProperties.Compute(voxel_brep).Centroid
          start_point = rs.coerce3dpoint(ld_centroid)
          end_point = rs.coerce3dpoint(voxel_centroid)
          
          vector = rg.Vector3d(end_point - start_point)
          
          rs.CopyObject(lowdensity, vector)



def split_breps_with_breps(breps_to_split, splitting_breps, brep):
    split_breps = []
    splitting_breps = splitting_breps.Surfaces
    for brep_to_split in breps_to_split:
        for splitting_brep in splitting_breps:
            splitting_brep = Rhino.Geometry.Brep.CreateFromSurface(splitting_brep)
            print(brep_to_split)
            if str(brep_to_split) == "Rhino.Geometry.Box":
                brep_to_split = rg.Brep.CreateFromBox(brep_to_split)
            intersection_curves = rg.Intersect.Intersection.BrepBrep(brep_to_split, splitting_brep, 0.001)
            if intersection_curves:
                #brep_pieces = (rs.SplitBrep(brep_to_split, splitting_brep))
                brep_pieces = (brep_to_split.CreateBooleanSplit(brep_to_split, splitting_brep, .001))
                    # Check if any pieces were created
                if brep_pieces:
                    #rs.DeleteObject(brep_to_split)
                    for piece in brep_pieces:
                        #test inside or outside
                        piece_centroid = rs.SurfaceVolumeCentroid(rs.coercebrep(piece))
                        if brep.IsPointInside(piece_centroid[0], .001, True):
                            print("The point is inside the Brep.")
                            split_breps.append(rs.coercebrep(piece))
                        else:
                            print("The point is not inside the Brep.")
                            
                        print("Brep split successful.")
                else:
                    print("No pieces were created.")

    return split_breps, brep_to_split

def is_point_on_brep(point, brep):
    """
    Check if a point is on any of the surfaces of a Brep.
    """
    # Get all the surfaces of the BrepSurfacesfaces
    surfaces = brep.Surfaces
    closesetPoint = brep.ClosestPoint(point)
    distance = point.DistanceTo(closesetPoint)
    if distance < 2:
        return True
    # If the point is not on any surface of the Brep
    return False




#points_guid = [rs.coerce3dpoint(points_guid) for point_guid in point_guids]
brep_guid = rs.GetObject("Select a Brep", rs.filter.surface | rs.filter.polysurface)
points_guid = rs.GetObjects("Select points", rs.filter.point)
voxel_size = rs.GetReal("Enter voxel size", 2.0)

rs.HideObject(brep_guid)
rs.HideObject(points_guid)

voxels, colors, voxel_guid = voxelize_brep(rs.coercebrep(brep_guid), voxel_size, points_guid)
#toolpath geometry 



#rs.HideObjects(voxel_guid)

#split_voxels, voxels = split_breps_with_breps(voxels, rs.coercebrep(brep_guid), rs.coercebrep(brep_guid))

highdensity = rs.GetObjects("Pick High Density Toolpath")
hd_centroid = rs.GetObject("Pick High Density centroid")

meddensity = rs.GetObjects("Pick Medium Density Toolpath")
md_centroid = rs.GetObject("Pick Medium Density centroid")

lowdensity = rs.GetObjects("Pick Low Density Toolpath")
ld_centroid = rs.GetObject("Pick Low Density centroid")

toolpath = toolpath_to_voxel(voxels, colors, highdensity, hd_centroid, meddensity, md_centroid, lowdensity, ld_centroid)
