import os, sys

def element_data_to_isotope_data(data):
    """
    Converts elemental weight fraction to a list of weight fractions adjusted for naturally occurring isotope
    percentages.
    :param data: iterable with length of 2 [element code(string), element weight fraction (float)]
    :return: 2d list with isotope codes paired with isotope weight fractions
    """

    element = data[0]
    weight_fraction_element = data[1]
    return_list = []

    # Creates a dictionary with element codes corresponding with a list of
    # naturally occurring isotope codes and percentages
    isotope_dict = dict()
    isotope_dict['1000'] = [['1001', 1]]
    isotope_dict['6000'] = [['6012', 0.9893],
                            ['6013', 0.0107]]
    isotope_dict['7000'] = [['7014', 0.99636],
                            ['7015', 0.00364]]
    isotope_dict['8000'] = [['8016', 1]]
    isotope_dict['11000'] = [['11023', 1]]
    isotope_dict['12000'] = [['12024', 0.7899],
                             ['12025', 0.1],
                             ['12026', 0.1101]]
    isotope_dict['15000'] = [['15031', 1]]
    isotope_dict['16000'] = [['16032', 0.9499],
                             ['16033', 0.0075],
                             ['16034', 0.0425],
                             ['16036', 0.0001]]
    isotope_dict['17000'] = [['17035', 0.7576],
                             ['17037', 0.2424]]
    isotope_dict['19000'] = [['19039', 0.932581],
                             ['19040', 0.000117],
                             ['19041', 0.067302]]
    isotope_dict['20000'] = [['20040', 0.96941],
                             ['20042', 0.00647],
                             ['20043', 0.00135],
                             ['20044', 0.02086],
                             ['20046', 0.00004],
                             ['20048', 0.00187]]
    isotope_dict['26000'] = [['26054', 0.05845],
                             ['26056', 0.91754],
                             ['26057', 0.02119],
                             ['26058', 0.00282]]
    isotope_dict['53000'] = [['52127', 1]]

    # Populates a list of isotope codes and weight percentages based on the data in isotope_dict
    for isotope in isotope_dict[element]:
        return_list.append([isotope[0], (isotope[1]*weight_fraction_element)])

    return return_list


def process_file(data, filename):
    """
    Creates a new file with the same format as the input file, but with changed data.
    The input file remains unchanged.
    :param data: List of lines from the input file
    :param filename: Name of the input file
    :return: None
    """

    # Not every line in the file contains useful data. Finds the useful lines and puts them into real_data
    index_data_start = data.index('c    Materials\n')+2
    index_data_end = data.index(
        "c    --------------------------------------------------------------------------\n",
        index_data_start
    )
    real_data = data[index_data_start:index_data_end]

    lines_for_output_file = []
    for line in real_data:

        # Separates data in the line into a list of values
        split_data = [a for a in line.split(' ') if a]

        # If the first element of split_data is a digit, material is blank, split_digit[0] is the element code,
        # split_data[1] is the weight fraction, and split_data[2] is the description
        if split_data[0].isdigit():
            material = ''
            element = split_data[0]
            weight_fraction = float(split_data[1])
            description = ' '.join(split_data[2:])

        # If the first element of split_data is a NOT a digit, split_data[0] is the material number
        # split_data[1] is the element code, split_data[2] is the weight fraction,
        # and split_data[3] is the description
        else:
            material = split_data[0]
            element = split_data[1]
            weight_fraction = float(split_data[2])
            description = ' '.join(split_data[3:])

        # 2d list of adjusted weight fractions returned from element_data_to_isotope_data
        try:
            all_isotope_data = element_data_to_isotope_data([element, weight_fraction])
        except KeyError:
            print("Invalid file:" + filename)
            exit(1)
        # Prepares data in a 2d list to be used during spreadsheet population
        lines_for_output_file.append([material, all_isotope_data[0][0], '%f' % all_isotope_data[0][1], description])
        for isotope_data_line in all_isotope_data[1:]:
            lines_for_output_file.append(['', isotope_data_line[0], '%f' % isotope_data_line[1], description])

    # Builds the proper file name and then opens the (possibly new) file with write permissions.
    raw_filename = filename[:filename.rfind(".")]
    file_extention = filename[filename.rfind(".") + 1:]
    outputfile = open(raw_filename + "_n." + file_extention, "w")
    print("Creating ", raw_filename + "_n." + file_extention)

    for line in data[:index_data_start]:
        outputfile.write(line)

    for line in lines_for_output_file:
        outputfile.write(line[0])
        outputfile.write(' ' * (8 - len(str(line[0]))))
        outputfile.write(line[1] + ' ' + str(line[2]))
        outputfile.write(' ' * (27 - 8 - len(line[1]) - len(str(line[2]))))
        outputfile.write(line[3])

    for line in data[index_data_end:]:
        outputfile.write(line)
    outputfile.close()


arr = []
file_names = []
file_name = ""
file_number = -1
"""
path = sys.argv[1]
print(str(sys.argv))
print(path)
"""

path = input()

for file_name in os.listdir(path):
    file_name = path + '\\' + file_name
    print(file_name)
    file_number += 1
    process_file(list(open(file_name)), file_name)

