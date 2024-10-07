import pandas as pd
import csv
import json
import os
import glob

#combine data into one file

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

    WARN: If newline='' is not specified, newlines '\n' or '\r\n' embedded inside quoted fields
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


def main():

    #import the csv or txt files, specify file type

    #imported in meters
    x_data = 'fea/data/x.txt'
    y_data = 'fea/data/y.txt'
    z_data = 'fea/data/z.txt'
    force_data = 'fea/data/stress.txt'

    x_csv = 'fea/data/x_data.csv'
    y_csv = 'fea/data/y_data.csv'
    z_csv = 'fea/data/z_data.csv'
    force_csv = 'fea/data/force_data.csv'
    all_data  = 'fea/data/pt_data.csv' 
 

    #x data
    read_file = pd.read_csv (x_data, sep='\t')
    read_file.to_csv (x_csv, index=None)

    x = read_csv(x_csv)
    y = read_csv(y_csv)
    z = read_csv(z_csv)

    pt_loc = []

    for line in x:



    #y data
    read_file = pd.read_csv (y_data, sep='\t')
    read_file.to_csv (y_csv, index=None)

    #z data
    read_file = pd.read_csv (z_data, sep='\t')
    read_file.to_csv (z_csv, index=None)

    #force data
    read_file = pd.read_csv (force_data, sep='\t')
    read_file.to_csv (force_csv, index=None)


    #combine data into one file
    path  = 'fea/data/'




    csv_data = read_csv(all_data)
    dict_data_x = read_csv_to_dicts(csv_data)
   


    output_file = 'fea/data/dataRAnsys.json'
    write_json(output_file, dict_data_x)







if __name__ == "__main__":
    main()