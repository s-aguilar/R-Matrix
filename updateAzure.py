import numpy as np
import pandas as pd
import argparse


def setw(num,var):
    return (' '*(num-len(var))+var)


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('file',type=str)
args = parser.parse_args()
original_file_name = args.file;
# print(original_file_name,type(original_file_name))


# Read in the parameters file and store its contents line by line in a list
parameters_file_line = []
with open('output/parameters.out') as f:
    for line in f:
        # print(line)
        parameters_file_line.append(line)

        # These edge cases do not ever exist
        # if(line.find('G-T Beta Decay') != -1): print('GT')
        # if(line.find('Fermi Beta Decay') != -1): print('Fermi')



# Find the number of 'J's in the file which is a proxy for number of levels
number_of_levels_in_parameters = 0
for ind,ele in enumerate(parameters_file_line):
    # 'ele' and 'parameters_file_line[ind]' are equivalent
    # return the lowest index where 'J' is found. If not, it returns -1.
    if(ele.find('J') != -1):
        number_of_levels_in_parameters += 1


# Read in energies and branching parameters
energy_list, type_list, value_list, units_list = [], [], [], []
list_length, energy_temp = 0, 0
for ind,ele in enumerate(parameters_file_line):
    # Empty line
    # Note end-of-line character is read as a single character
    if(ele == '\n'):
    # if(len(ele) == 1):
      energy_list.append(0.);
      type_list.append('L');
      value_list.append(0.);
      units_list.append('');
      list_length += 1;

    # Found a level
    elif(ele.find('J =') != -1):
        # print(ele.split())
        # example output:
        # ['J','=','6.0+','E_level','=','50.0000','MeV','ITERATIONS','=','0']
        line_split = ele.split()

        J_pi = line_split[2]
        E_level = line_split[5]
        unit_E = line_split[6]
        energy_temp = E_level
        # print(J_pi,E_level,unit_E,energy_temp)

    # Found channels in a level / handle edge cases
    # elif(ele.find('R =') != -1 and not
    #     (ele.find('G-T Beta Decay') != -1 or ele.find('Fermi Beta Decay') != -1)
    #     ):
    elif(ele.find('R =') != -1):
        # print(ele.split())
        # example output:
        # ['R','=','5','l','=','4','s','=','2.0','G','=','0.000000e+00','meV',
        #  'g_int','=','0.000000e+00','MeV^(1/2)','g_ext','=',
        #  '(0.000000e+00,0.000000e+00)','MeV^(1/2)']
        line_split = ele.split()

        R = line_split[2]
        l = line_split[5]
        s = line_split[8]
        G = np.float64(line_split[11])
        G_unit = line_split[12]
        g_int = np.float64(line_split[15])

        # Note 'sign' returns 0 if 'g_int' is 0
        sign = np.sign(g_int)
        # print(R,l,s,g_int,sign)

        energy_list.append(energy_temp)
        type_list.append('R')
        if(G_unit == 'meV'):
          value_list.append(str(sign*G/1000.))
        elif(G_unit == 'eV'):
          value_list.append(str(sign*G))
        elif(G_unit== 'keV'):
          value_list.append(str(sign*G*1000.))
        else:
          value_list.append(str(sign*G))

        units_list.append(G_unit)
        list_length += 1


    # Found beta-delayed channel in level
    # elif(ele.find('R =') != -1 and
    #     (ele.find('G-T Beta Decay') != -1 or ele.find('Fermi Beta Decay') != -1)
    #     ):
    # elif(ele.find('R '') != -1):
    #     pass


# Read in the input azure file that was passed in argument
original_input_file_line = []
with open(original_file_name) as f:
    for line in f:
        # print(line)
        original_input_file_line.append(line)


# Find beginning and end of nuclear input in the azure file
start_flag, end_flag = 0 , 0
for ind,ele in enumerate(original_input_file_line):
    if(ele == '<levels>\n'): start_flag = ind
    elif(ele == '</levels>\n'): end_flag = ind


# Find how many levels are in nuclear file
number_of_levels_in_nuclear_file = 0
for ind,ele in enumerate(original_input_file_line):
    # Note end-of-line character is read as a single character
    # if(ele == ''):
    if(ele == '\n'):
        number_of_levels_in_nuclear_file += 1


# Check to see if the input has the same levels as in the azure file
if(number_of_levels_in_nuclear_file != number_of_levels_in_parameters):
    print('Number of levels in parameter file does not match number of levels in nuclear file!')
    print('Number of levels in parameter =',number_of_levels_in_parameters)
    print('Number of levels in nuclear file =',number_of_levels_in_nuclear_file)
    exit()
else: print('Parameters updated')


# Shift indexing in nuclear input file
# original_input_file_line_mod = []
original_input_file_line_mod = original_input_file_line[ind+start_flag::]
# print(original_input_file_line_mod)

# original_input_file_line_mod = []
# for ind in range(end_flag-start_flag):
#     original_input_file_line_mod.append(original_input_file_line[ind+start_flag])

# print(original_input_file_line_mod)


# Make new input file
with open('temp.azr','w') as f:
    for ind,ele in enumerate(original_input_file_line):
        if(ind <= start_flag):
            f.write(ele)
        elif(ind > start_flag and ind < end_flag and
            ele != '\n'):
            spl = ele.split()   # There are 31 elements
            # print(spl)
            channelFix_ = spl[10]
            if(channelFix_ == 1):
                f.write(setw(4,spl[0]) +
                        setw(5,spl[1]) +
                        setw(13,energy_list[ind-startflag]) +
                        setw(5,spl[3]) +
                        setw(5,spl[4]) +
                        setw(5,spl[5]) +
                        setw(5,spl[6]) +
                        setw(5,spl[7]) +
                        setw(5,spl[8]) +
                        setw(5,spl[9]) +
                        setw(5,spl[10]) +
                        setw(20,spl[11]) +
                        setw(5,spl[12]) +
                        setw(5,spl[13]) +
                        setw(5,spl[14]) +
                        setw(5,spl[15]) +
                        setw(13,spl[16]) +
                        setw(8,spl[17]) +
                        setw(8,spl[18]) +
                        setw(5,spl[19]) +
                        setw(5,spl[20]) +
                        setw(13,spl[21]) +
                        setw(13,spl[22]) +
                        setw(5,spl[23]) +
                        setw(5,spl[24]) +
                        setw(13,spl[25]) +
                        setw(6,spl[26]) +
                        setw(8,spl[27])+
                        setw(13,spl[28]) +
                        setw(13,spl[29]) +
                        setw(8,spl[30]) + '\n' )
            else:
                f.write(setw(4,spl[0]) +
                        setw(5,spl[1]) +
                        setw(13,energy_list[ind-start_flag]) +
                        setw(5,spl[3]) +
                        setw(5,spl[4]) +
                        setw(5,spl[5]) +
                        setw(5,spl[6]) +
                        setw(5,spl[7]) +
                        setw(5,spl[8]) +
                        setw(5,spl[9]) +
                        setw(5,spl[10]) +
                        setw(20,value_list[ind-start_flag]) +
                        setw(5,spl[12]) +
                        setw(5,spl[13]) +
                        setw(5,spl[14]) +
                        setw(5,spl[15]) +
                        setw(13,spl[16]) +
                        setw(8,spl[17]) +
                        setw(8,spl[18]) +
                        setw(5,spl[19]) +
                        setw(5,spl[20]) +
                        setw(13,spl[21]) +
                        setw(13,spl[22]) +
                        setw(5,spl[23]) +
                        setw(5,spl[24]) +
                        setw(13,spl[25]) +
                        setw(6,spl[26]) +
                        setw(8,spl[27]) +
                        setw(13,spl[28]) +
                        setw(13,spl[29]) +
                        setw(8,spl[30]) + '\n' )
        else:
            f.write(ele)

print('Done!')
