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


mdl = Structure(name='test', path='./test')  # make an empty/base structure

#mesh = rs.ObjectsByLayer('base_mesh')[0]  # grab the mesh from layer 'mesh'

mesh = rs.ObjectsByLayer('vol_mesh')[0]  # grab the coarse mesh from the workspace
layer = 'output'
target = 0.050
min_angle = 15

print(mesh)


rhino.add_tets_from_mesh(structure=mdl, name='elset_tets', mesh=mesh,
                         draw_tets=True, volume=0.5)  # make and add tet
                         