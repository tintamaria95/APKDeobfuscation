import subprocess
from parser_javap import parse_javap
from pathlib import Path
from tqdm import tqdm
import csv
import os


def get_instructions_from_jars(root_path: Path, app_name: str, is_obf: bool):
    '''
    This function takes the path to the folder containing the JARs of original
    and obfuscated app JARs and the csv files to make the mapping between both
    JARs. Each JAR contains java classes and respective methods. This function
    aims to retrieve the machine instructions of each methods and create a
    copy of the mapping csv with instructions.
    '''
    # extract the JAR into a temporary folder "app_name"
    # subprocess.run(["cd", root_path])
    suffix = ''
    if is_obf:
        suffix = '_out'
    subprocess.run(["mkdir", app_name], cwd=root_path)
    subprocess.run(["cp", f'{app_name}-dex2jar{suffix}.jar', f'{app_name}'],
                   cwd=root_path)
    subprocess.run(
        ["jar", "xf", f'{app_name}-dex2jar{suffix}.jar'],
        cwd=Path(root_path, app_name))

    # open csv to save instructions
    if not is_obf:
        csv_name = f'../csv_files/{app_name}.csv'
    else:
        csv_name = f'../csv_files/{app_name}_obf.csv'
    csvfile = open(csv_name, 'w', newline='')
    fieldnames = ['class_name', 'meth_name', 'instruction', 'ref']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if os.stat(csv_name).st_size == 0:
        writer.writeheader()

    # Use the csv mapping file to decompile each class
    with open(Path(root_path, f'{app_name}-dex2jar.csv')) as csvfile:
        reader = csv.DictReader(csvfile)
        decompile_classes = []
        cpt = 1
        for row in tqdm(reader):
            if not is_obf:
                class_name = row['class_int'].replace('.', '/')
            else:
                class_name = row['class_out'].replace('.', '/')

            is_already_decompiled = class_name in decompile_classes
            if is_already_decompiled:
                continue

            # decompile class file
            javap_txt = subprocess.run(
                ['javap', '-v', class_name],
                cwd=Path(root_path, app_name),
                capture_output=True
            ).stdout.decode("utf-8")
            # print(javap_txt)
            # parse it to retrieve instructions
            parsed_javap_txt = parse_javap(javap_txt)
            if parsed_javap_txt != []:
                save_to_csv(writer, class_name, parsed_javap_txt)
            decompile_classes.append(class_name)
            cpt += 1
            if cpt % 20 == 0:
                size_limit = 100
                if os.stat(csv_name).st_size > size_limit * 10e6:
                    break

    # Delete the teoporary folder with extracted files
    subprocess.run(
        ['rm', '-r', '-f', app_name], cwd=root_path)
    print(cpt)


def save_to_csv(
        writer: csv.DictWriter,
        class_name: str,
        parsed_javap_txt: str):

    for method in parsed_javap_txt:
        for instruction in method[1]:
            writer.writerow({
                'class_name': class_name,
                'meth_name': method[0],
                'instruction': instruction[0],
                'ref': instruction[1]
            })


def get_apk_names(root_folder: Path):
    return [x[: -4] for x in os.listdir(root_folder) if x.find('.apk') != -1]


if __name__ == "__main__":
    root_path = "/home/tintamaria95/Documents/Graphics"
    # app_names = get_apk_names(root_path)
    app_names = [str(x[:-4])
                 for x in os.listdir('../csv_files')]
    for app_name in app_names:
        # if str(app_name + '.csv') not in os.listdir('../csv_files'):
        get_instructions_from_jars(root_path, app_name, True)
