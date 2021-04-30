import sys
import os
import argparse
import logging
import shutil
import platform
import pkg_resources
import stat
import ntpath

from ament_index_python import get_package_prefix, get_package_share_directory
from ament_index_python.packages import PackageNotFoundError


class UnityROS2LibCopier:
    def __init__(self, output_path):
        self.ament_dependencies = [
            'rcl',
            'rcl_interfaces',
            'rmw',
            'rmw_implementation',
            'rmw_cyclonedds_cpp',
            'rosidl_generator_c',
            'rosidl_typesupport_c',
            'rosidl_typesupport_cpp',
            'rcl_logging_noop',
            'rosidl_typesupport_introspection_c',
            'rosidl_typesupport_introspection_cpp',
            'builtin_interfaces',
            'rcutils',
            'rcldotnet',
            'std_msgs',
            'geometry_msgs',
            'sensor_msgs',
            'nav_msgs',
            'test_msgs',
            'action_msgs',
            'unique_identifier_msgs',
            'marker_msgs',
            'marker_planner_msgs',
            'gis_rtk_msgs',
            'rtp_msgs',
            'tf2_msgs',
        ]

        self.dependencies = [
            'cyclonedds'
        ]

        self.c_lib_source_dict = {}
        if platform.system() == 'Windows':
            self.c_lib_destination_dir = output_path + '/Plugins/Windows/x86_64'
        else:
            self.c_lib_destination_dir = output_path + '/Plugins/Linux/x86_64'

        self.cs_lib_source_dict = {}
        self.cs_lib_destination_dir = output_path + '/Plugins'

        self.__find_libs()

    def copy_files(self):
        self.__copy_files_from_dict(self.c_lib_source_dict,
                                    self.c_lib_destination_dir)

        self.__copy_files_from_dict(self.cs_lib_source_dict,
                                    self.cs_lib_destination_dir)

    def __find_libs(self):
        self.__find_c_libs()
        self.__find_csharp_libs()

    def __find_c_libs(self):
        for package_name in self.ament_dependencies:
            try:
                package_install_path = get_package_prefix(package_name)
                package_install_parent_directory = os.path.abspath(
                    os.path.join(package_install_path, os.pardir))

                if platform.system() == 'Windows':
                    filename_extensions = ('.dll')
                    lib_folder = '\\bin'
                    package_lib_path = package_install_path + lib_folder
                else:
                    filename_extensions = ('.so')
                    lib_folder = '/lib'
                    package_lib_path = package_install_path + lib_folder

                if os.path.isdir(package_lib_path):
                    for c_lib_file in os.listdir(package_lib_path):
                        if c_lib_file.endswith(filename_extensions):
                            self.c_lib_source_dict[c_lib_file] = (
                                package_lib_path + '/' + c_lib_file)

                # Find ament compiled projects not found by ament_index
                # by looking in parent folders of ros install directories
                for non_ros_package in self.dependencies:
                    if non_ros_package in os.listdir(package_install_parent_directory):
                        lib_path = package_install_parent_directory + '/' + non_ros_package + lib_folder
                        if os.path.isdir(lib_path):
                            try:
                                for c_lib_file in os.listdir(lib_path):
                                    if c_lib_file.endswith(filename_extensions):
                                        self.c_lib_source_dict[c_lib_file] = (
                                            lib_path + '/' + c_lib_file)
                            except PackageNotFoundError:
                                pass

            except PackageNotFoundError:
                print('{} not found!'.format(package_name))

    def __find_csharp_libs(self):
        for package_name in self.ament_dependencies:
            try:
                package_install_path = get_package_prefix(package_name)
                package_lib_path = package_install_path + '/lib/dotnet'
                if os.path.isdir(package_lib_path):
                    for csharp_lib_file in os.listdir(package_lib_path):
                        if csharp_lib_file.endswith('.dll'):
                            self.cs_lib_source_dict[csharp_lib_file] = (
                                package_lib_path + '/' + csharp_lib_file)
            except PackageNotFoundError:
                print('{} not found!'.format(package_name))

    def __copy_files_from_dict(self, source_dictionary, destination_directory):
        if not os.path.isdir(destination_directory):
            try:
                os.makedirs(destination_directory)
            except OSError:
                logging.error('Failed to create directory {}'.format(
                    destination_directory))
            else:
                logging.info('Successfully created the directory {}'.format(
                    destination_directory))

        for filename, source_path in source_dictionary.items():
            destination_path = destination_directory + '/' + filename
            if should_copy_file(source_path, destination_path):
                logging.info('Copying "{}"'.format(filename))
                shutil.copy2(source_path, destination_path)

def should_copy_file(source_path, destination_path):

    def does_not_exist(destination_path):
        return not os.path.isfile(destination_path)

    def newer_verson_available(source_path, destination_path):
        return (os.stat(source_path).st_mtime
                - os.stat(destination_path).st_mtime > 0)

    return (does_not_exist(destination_path)
            or newer_verson_available(source_path, destination_path))

def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--path', default=os.getcwd(), help='path to where plugin should be copied'
    )

    return parser.parse_args(args)

def main():
    logging.basicConfig(level=logging.DEBUG)

    parsed = parse_args(sys.argv[1:])

    lib_copier = UnityROS2LibCopier(parsed.path)
    lib_copier.copy_files()


if __name__ == '__main__':
    main()
