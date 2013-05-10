#! /usr/bin/env python

from argparse import ArgumentParser
import os
import re
from pprint import pprint
from subprocess import Popen, PIPE
import subprocess

scripts_folder = "/var/www/beta/scripts/"
os.chdir(scripts_folder)

ignored_folders = [
    './dev',
]

module_list_filename = "main-production.js"
build_filename = "../build.js"


def get_files_recursive():
    js_files = []
    for root, subFolders, files in os.walk("."):
        if root in ignored_folders:
            break
        for file in files:
            if is_javascript(file):
                filepath = os.path.join(root, file)
                js_files.append(filepath)
    return js_files


def is_javascript(file):
    extension_with_dot = file[-3:]
    return extension_with_dot == ".js"


def filter_out_start_path(js_files):
    filtered = []
    for file in js_files:
        replaced = re.sub("^\./", "", file)
        filtered.append(replaced)
    return filtered


def filter_extension(js_files):
    filtered = []
    for file in js_files:
        filtered.append(file.replace(".js", ""))
    return filtered


def get_requirejs_define_statement(js_files):
    start = "require([\n\t'"
    center = "',\n\t'".join(js_files)
    end = "']);\n"
    return "".join([start, center, end])


def write_statement(string):
    with open(module_list_filename, "w") as file:
        file.write(string)


def run_compressor():
    cmd = ["r.js", "-o", build_filename]
    process = Popen(cmd, stdout=PIPE)
    for line in process.stdout:
        print(line.decode("utf-8"), end="")


def remove_module_list():
    os.remove(module_list_filename)


def run():
    js_files = get_files_recursive()
    js_files = filter_out_start_path(js_files)
    js_files = filter_extension(js_files)
    define_statement = get_requirejs_define_statement(js_files)
    write_statement(define_statement)
    run_compressor()
    remove_module_list()

run()
