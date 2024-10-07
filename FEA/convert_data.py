import json
import csv

class StructuralData:
    """Represents a the node data extracted from Ansys Discovery.

    Attributes:
        node (str): node number
        point location (tuple): (x, y, z) 
        stress (float): stress data for each node

    Methods:
        jsonable: return JSON-friendly dict representation of the object
    """

    def __init__(self):
        """Initialize an instance."""

        self.node = []
        self.coordinates = []
        self.stress = []

    def __str__(self):
        """Return a string representation of the object."""

        return self.type

    def jsonable(self):

        return {
            'Node': self.node,
            'coordinates': self.coordinates,
            'stress': self.stress,
        }

def convert_to_float(value):
    """Attempts to convert a string or a number < value > to a float. If unsuccessful or an
    exception is encountered returns the < value > unchanged. Note that this function will
    return True for boolean values, faux string boolean values (e.g., "true"), "NaN", exponential
    notation, etc.

    Parameters:
        value (obj): string or number to be converted

    Returns:
        float: if value successfully converted; otherwise returns value unchanged
    """

    if type(value) is list:
        for item in value:
            if type(item) is str:
                try:
                    float(item)
                except:
                    continue
        return value

    elif type(value) is str:
        try:
            value = float(value)
            return value
        except:
            return value
    else:
        return value


def convert_to_int(value):
    """Attempts to convert a string or a number < value > to an int. If unsuccessful or an
    exception is encountered returns the < value > unchanged. Note that this function will return
    True for boolean values, faux string boolean values (e.g., "true"), "NaN", exponential
    notation, etc.

    Parameters:
        value (obj): string or number to be converted

    Returns:
        int: if value successfully converted; otherwise returns value unchanged
    """
    if type(value) is list:
        for item in value:
            if type(item) is str:
                try:
                    int(item)
                except:
                    continue
        return value

    elif type(value) is str:
        try:
            value = int(value)
            return value
        except:
            return value
    
    else:
        return value

def read_csv(filepath, encoding='utf-8', newline='', delimiter=','):
    """
    Reads a CSV file, parsing row values per the provided delimiter. Returns a list of lists,
    wherein each nested list represents a single row from the input file.

    WARN: If a byte order mark (BOM) is encountered at the beginning of the first line of decoded
    text, call < read_csv > and pass 'utf-8-sig' as the < encoding > argument.

    WARN: If newline='' is not specified, newlines '\n' or '\r\n' embedded inside quoted fields
    may not be interpreted correctly by the csv.reader.

    Parameters:
        filepath (str): The location of the file to read
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: a list of nested "row" lists
    """

    with open(filepath, 'r', encoding=encoding, newline=newline) as file_obj:
        data = []
        reader = csv.reader(file_obj, delimiter=delimiter)
        for row in reader:
            data.append(row)

        return data
    
def text_to_csv(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in lines:
            values = line.split()
            writer.writerow(values)

def read_csv_to_dicts(filepath, encoding='utf-8', newline='', delimiter=','):
    """Accepts a file path, creates a file object, and returns a list of dictionaries that
    represent the row values using the cvs.DictReader().

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: nested dictionaries representing the file contents
     """

    with open(filepath, 'r', newline=newline, encoding=encoding) as file_obj:
        data = []
        reader = csv.DictReader(file_obj, delimiter=delimiter)
        for line in reader:
            data.append(line) # OrderedDict()
            # data.append(dict(line)) # convert OrderedDict() to dict

        return data

def read_json(filepath, encoding='utf-8'):
    """Reads a JSON document, decodes the file content, and returns a list or dictionary if
    provided with a valid filepath.

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file

    Returns:
        dict/list: dict or list representations of the decoded JSON document
    """

    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)


def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    """Serializes object as JSON. Writes content to the provided filepath.

    Parameters:
        filepath (str): the path to the file
        data (dict)/(list): the data to be encoded as JSON and written to the file
        encoding (str): name of encoding used to encode the file
        ensure_ascii (str): if False non-ASCII characters are printed as is; otherwise
                            non-ASCII characters are escaped.
        indent (int): number of "pretty printed" indention spaces applied to encoded JSON

    Returns:
        None
    """

    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)



def create_point(data):

    newpoint = {}

    for key, value in data.items():
        if key == "LOCX (m)":
            value = convert_to_float(value)
            newpoint.update({'coordinate': value})

def main():
    print("meow")
    

    #convert text file into a dict
    pt_data = 'fea/data/wall003NLIST.txt'

    pt_csv = 'fea/data/pt_data.csv'

    text_to_csv(pt_data, pt_csv)

    

    pt_data = read_csv_to_dicts(pt_data, delimiter=' ')
    write_json('pt_data.json', pt_data)

    pt_json = './pt_data.json'

    pt_json = read_json(pt_json, encoding='utf-8')
    ansys = StructuralData()

    for i in range(len(pt_json)):
        #print(type(x_json[i]))
        for key, value in pt_json[i].items():
            if key == "X":
                value = convert_to_float(value)
                #convert to inch
                value = value*39.3701
                ansys.coordinates.append([value, 'none' , 'none'])

    """    
    #convert text file into a dict
    x_data = 'fea/data/x.txt'

    x_csv = 'fea/data/x_data.csv'

    x_data = read_csv_to_dicts(x_data, delimiter='\t')
    write_json('x_data.json', x_data)

    x_json = './x_data.json'

    x_json = read_json(x_json, encoding='utf-8')
    ansys = StructuralData()

    for i in range(len(x_json)):
        #print(type(x_json[i]))
        for key, value in x_json[i].items():
            if key == "LOCX (m)":
                value = convert_to_float(value)
                #convert to inch
                value = value*39.3701
                ansys.coordinates.append([value, 'none' , 'none'])

    y_data = 'fea/data/y.txt'

    y_csv = 'fea/data/y_data.csv'

    y_data = read_csv_to_dicts(y_data, delimiter='\t')
    write_json('y_data.json', y_data)

    y_json = './y_data.json'

    y_json = read_json(y_json, encoding='utf-8')

    for i in range(len(y_json)):
        #print(type(y_json[i]))
        for key, value in y_json[i].items():
            if key == "LOCY (m)":
                value = convert_to_float(value)
                #convert to inch
                value = value*39.3701
                ansys.coordinates[i][1] = value

    z_data = 'fea/data/z.txt'

    z_csv = 'fea/data/z_data.csv'

    z_data = read_csv_to_dicts(z_data, delimiter='\t')
    write_json('z_data.json', z_data)

    z_json = './z_data.json'

    z_json = read_json(z_json, encoding='utf-8')

    for i in range(len(z_json)):
        #print(type(z_json[i]))
        for key, value in z_json[i].items():
            if key == "LOCZ (m)":
                value = convert_to_float(value)
                #convert to inch
                value = value*39.3701
                ansys.coordinates[i][2] = value """
    
    #stress data 
    stress_data = 'fea/data/wall003vonmies.txt'

    stress_csv = 'fea/data/stress_data.csv'

    stress_data = read_csv_to_dicts(stress_data, encoding='unicode_escape', delimiter='\t')
    write_json('stress_data.json', stress_data)

    stress_json = './stress_data.json'

    stress_json = read_json(stress_json, encoding='unicode_escape')

    for i in range(len(stress_json)):
        #print(type(z_json[i]))
        for key, value in stress_json[i].items():
            if key == "Maximum Principal Stress (Pa)":
                value = convert_to_float(value)

                ansys.stress.append(value)

    #start rhino and add poionts to document

    import rhinoinside
    rhinoinside.load()
    import System


    import rhino3dm
    #import System
    from Rhino import RhinoDoc
    from Rhino import DocObjects
    from Rhino import Geometry
    
    model = rhino3dm.File3dm()   
    low_stress_attr = rhino3dm.ObjectAttributes()
    medium_stress_attr = rhino3dm.ObjectAttributes()
    high_stress_attr = rhino3dm.ObjectAttributes()

    # Create a new point with custom attrs.

    # create and add layer
    low_stress = rhino3dm.Layer()
    medium_stress = rhino3dm.Layer()
    high_stress = rhino3dm.Layer()


    pts = ansys.coordinates
    stress = ansys.stress
    count_low = 0
    pt_low = []
    count_med = 0
    pt_med = []
    count_high = 0
    pt_high = []


    model.Layers.AddLayer('low_stress', (190, 255, 72, 255))

    model.Layers.AddLayer('medium_stress', (255, 242, 161, 255))

    model.Layers.AddLayer('high_stress', (255, 0, 118, 255))

    low_stress_attr.Name = 'low_stress'
    low_stress_attr.ObjectColor = (190, 255, 72, 255)



    medium_stress_attr.Name = 'medium_stress'
    medium_stress_attr.ObjectColor = (255, 242, 161, 255)



    high_stress_attr.Name = 'high_stress'
    high_stress_attr.ObjectColor = (255, 0, 118, 255)



    doc = RhinoDoc.CreateHeadless("")

    file = RhinoDoc.Path


    rhinofile = 'G:/.shortcut-targets-by-id/1FAU4THzIvFnKiKL_t-YA0eWgH2EbD29H/UMICH_DART/08-PhD Research/01-Christopher_Voltl/00-Projects/Functionally_graded_Multimaterial/01-Models/00-Rhino/rhinopy.3dm'

    #doc.Import(rhinofile)
    #pts = System.Collections.Generic.List[Geometry.Point3d]()



    for i in range(len(pts)):
        #pt = tuple(pt)        
        if stress[i] < 50:
            attrs = DocObjects.ObjectAttributes()
            attrs.LayerIndex = 0
            attrs = DocObjects.ObjectAttributes()
            attrs.ColorSource = DocObjects.ObjectColorSource.ColorFromObject
            attrs.ObjectColor = System.Drawing.Color.Green
            pt = doc.Objects.AddPoint(Geometry.Point3d(pts[i][0], pts[i][1], pts[i][2]), attrs)
            #pt_low.append(new_pt.urn[9:])
            count_low = count_low + 1
            
    
            

        if 50.1 > stress[i] < 100:
            attrs = DocObjects.ObjectAttributes()
            attrs.LayerIndex = 1
            attrs.ColorSource = DocObjects.ObjectColorSource.ColorFromObject
            attrs.ObjectColor = System.Drawing.Color.Yellow
            pt = doc.Objects.AddPoint(Geometry.Point3d(pts[i][0], pts[i][1], pts[i][2]), attrs)
            #pt_med.append(new_pt.urn[9:])
            count_med = count_med + 1

            

        if stress[i] > 101:
            attrs = DocObjects.ObjectAttributes()
            attrs.LayerIndex = 2
            attrs.ColorSource = DocObjects.ObjectColorSource.ColorFromObject
            attrs.ObjectColor = System.Drawing.Color.Red
            pt = doc.Objects.AddPoint(Geometry.Point3d(pts[i][0], pts[i][1], pts[i][2]), attrs)
            #pt_high.append(new_pt.urn[9:])
            count_high = count_high + 1

    #doc.Views.ActiveView.Redraw()




    for layer in model.Layers:
        print('Name = {0}, Id = {1}'.format(layer.Name, layer.Id))

    print (count_low, count_med, count_high)

    rhVersion = 7
    #model.Write(rhinofile, rhVersion)
    doc.Export(rhinofile)

if __name__ == '__main__':
    main()
