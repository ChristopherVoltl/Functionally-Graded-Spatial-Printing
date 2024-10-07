from compas.datastructures import Mesh
from compas.geometry import distance_point_point
#from compas_rhino.helpers import mesh_from_guid

from compas_fea.cad import rhino
from compas_fea.structure import BucklingStep
from compas_fea.structure import Concrete
from compas_fea.structure import ElementProperties as Properties
from compas_fea.structure import GeneralStep
from compas_fea.structure import GravityLoad
from compas_fea.structure import PointLoad
from compas_fea.structure import RectangularSection
from compas_fea.structure import RollerDisplacementY
from compas_fea.structure import ShellSection
from compas_fea.structure import Steel
from compas_fea.structure import Structure
from compas_fea.structure import TrussSection

import rhinoscriptsyntax as rs

mdl = Structure(name='test', path='./test')  # create an empty Structure with name and path

#mdl.summary()

#mdl.save_to_obj(output=True)

#Node data is fundamental to the Structure, and is stored in the .nodes attribute as a dictionary of Node objects 
mdl.add_nodes(nodes=[[5, -5, 0], [5, 5, 0], [-5, 5, 0], [0, 0, 5]])

#The nodes data are Node objects stored in the .nodes dictionary, and are added with integer keys numbered sequentially starting from 0 (Python based). 
#The data summary for each node can be viewed by printing the Node to the terminal.

#print(mdl.nodes[3])

nodecount = mdl.node_count()
print(nodecount)

node_bounds = mdl.node_bounds()  # return [xmin, xmax], [ymin, ymax], [zmin, zmax]
print(node_bounds)

node_index = mdl.node_index  # show the current node index dictionary
print(node_index)



#MESH

mesh = rs.ObjectsByLayer('base_vol_mesh')[0]  # grab the mesh from layer 'mesh'

rhino.add_tets_from_mesh(structure=mdl, name='elset_tets', mesh=mesh,
                         draw_tets=True, volume=0.1)  # make and add tets