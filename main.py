#!/usr/bin/python3

import argparse
import os
from pathlib import Path
from shutil import move
import logging
import configparser
import glob


def create_directories(base_directory, jpeg_directory, raw_directory, edits_directory):
    directories_to_create = list()

    directories_to_create.append(os.path.join(base_directory, jpeg_directory))
    directories_to_create.append(os.path.join(base_directory, raw_directory))
    directories_to_create.append(os.path.join(base_directory, edits_directory))

    for directory in directories_to_create:
        if not os.path.isdir(directory):
            print(f'Creating {directory}')
            os.mkdir(directory)
        else:
            print(f'{directory} already exists. Skipping creation.')


def sort_files(base_directory, jpeg_directory, jpeg_extension, raw_directory, raw_extension):
    jpegs = glob.glob(os.path.join(base_directory, f'*{jpeg_extension}'))
    for jpeg in jpegs:
        print(f'Moving {jpeg} to {jpeg_directory}.')
        move(jpeg, os.path.join(base_directory, jpeg_directory))

    raws = glob.glob(os.path.join(base_directory, f'*{raw_extension}'))
    for raw in raws:
        print(f'Moving {raw} to {raw_directory}.')
        move(raw, os.path.join(base_directory, raw_directory))


def delete_files(base_directory, jpeg_directory, raw_directory, ignore_hidden_files):
    approved_jpegs = list()

    for base, dirs, files in os.walk(os.path.join(base_directory, jpeg_directory)):
        for file in files:
            if ignore_hidden_files:
                if not file.startswith('.'):
                    approved_jpegs.append(Path(file).stem)
            else:
                approved_jpegs.append(Path(file).stem)

    for base, dirs, files in os.walk(os.path.join(base_directory, raw_directory)):
        for file in files:
            full_file_path = os.path.join(base, file)
            if Path(file).stem not in approved_jpegs:
                print(f'Deleting {full_file_path}')
                os.remove(full_file_path)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--photo_directory', '-p', required=True)
    parser.add_argument('--config_file', '-c', default='photoflow.cfg')
    args = parser.parse_args()

    photoflow_config = configparser.ConfigParser()
    photoflow_config.read(args.config_file)
    jpeg_directory = photoflow_config["basic_configuration"]["jpeg_directory"]
    raw_directory = photoflow_config["basic_configuration"]["raw_directory"]
    edits_directory = photoflow_config["basic_configuration"]["edits_directory"]
    jpeg_file_extension = photoflow_config["basic_configuration"]["jpeg_file_extension"]
    raw_file_extension = photoflow_config["basic_configuration"]["raw_file_extension"]
    ignore_hidden_files = bool(photoflow_config["basic_configuration"]["ignore_hidden_files"])

    create_directories(args.photo_directory, jpeg_directory, raw_directory, edits_directory)

    sort_files(args.photo_directory, jpeg_directory, jpeg_file_extension, raw_directory, raw_file_extension)

    delete_files(args.photo_directory, jpeg_directory, raw_directory, ignore_hidden_files)


if __name__ == '__main__':
    main()
