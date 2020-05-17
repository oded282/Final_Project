import re


# This function used to create to files from the animal dictionary we find in the internet.
# The dictionary contains an animal common name, and the scientific name related to the common one.
# We separated the names into two files, common names file and scientific names file.
def create_animals_files(all_animals_file, common_names_file, scientific_names_file):
    with open(all_animals_file) as ofd:
        with open(common_names_file, 'w') as rfd:
            with open(scientific_names_file, 'w') as sfd:
                line = ofd.readline()
                regular_name = True
                dict = []
                while line:
                    line = line.strip('\n')
                    match = re.fullmatch('[A-Z]top', line)

                    if "(unidentified)" in line:
                        line = line.split(' ')[0]

                    if ',' in line:
                        names = line.split(',')
                        line = (names[0])

                    if line != '' and match is None and line not in dict:
                        if regular_name:
                            line = line.split(' ')[-1]
                            rfd.write(line.lstrip().rstrip() + '|')
                            regular_name = False
                        else:
                            sfd.write(line.lstrip().rstrip() + '|')
                            regular_name = True

                        dict.append(line)

                    line = ofd.readline()