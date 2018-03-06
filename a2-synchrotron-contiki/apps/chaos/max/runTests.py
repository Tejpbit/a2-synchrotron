#!/bin/python
import subprocess
import os
import shlex
import sys
import datetime
import xml.etree.ElementTree as ET

RUN_TEST_COMMAND = ["./runTest"]
TEST_DIRECTORY = "tests"
GLOBAL_SIMULATION_DIRECTORY = TEST_DIRECTORY + "/Simulations"

TEST_FILE_EXTENSION = ".csc"
SCRIPT_TAG = ".//script"
SCRIPT_FILE = TEST_DIRECTORY + "/" + "simulationScript.js"

LOCAL_SIMULATION_DIRECTORY = "simulation_files"
LOCAL_LOG_DIRECTORY = "log"
LOCAL_COOJA_LOG_FILE = "cooja.log"
#Time is in seconds.
SIMULATION_TIMEOUT = 60

def get_global_simulation_files(folder):
  return [file for root, dirs, files in os.walk(folder) for file in files if file.endswith(TEST_FILE_EXTENSION) ]

def create_test_folder_structure(test_name):
  test_folder = TEST_DIRECTORY + "/" + test_name + str(datetime.datetime.now())
  simulation_folder = test_folder + "/" + LOCAL_SIMULATION_DIRECTORY

  os.mkdir(test_folder)
  os.mkdir(simulation_folder)

  return test_folder, simulation_folder

def create_local_test_folder(test_directory, simulation_file):
  folder_name = os.path.splitext(os.path.basename(simulation_file))[0]
  local_test_folder = test_directory + "/" + folder_name
  log_folder = local_test_folder + "/" + LOCAL_LOG_DIRECTORY

  os.mkdir(local_test_folder)
  os.mkdir(log_folder)

  return local_test_folder

def create_log_path_variable(base_path, file_name):
  return "var logpath = \"" + base_path + "/" + os.path.splitext(file_name)[0] + "/" + LOCAL_LOG_DIRECTORY + "/\"\n"

def create_timeout_function_call(time):
  return "TIMEOUT( + " + str(time * 1000) + ");\n"

def create_local_simulation_files(test_folder, output_folder):
  simulation_files = get_global_simulation_files(GLOBAL_SIMULATION_DIRECTORY)
  simulation_script = ""
  local_files = []

  with open (SCRIPT_FILE) as file:
    simulation_script = file.read()

  for simulation_file in simulation_files:
    output_file = output_folder + "/" + simulation_file
    tree = ET.parse(simulation_file)
    root = tree.getroot()

    script_tag = root.find(SCRIPT_TAG)
    log_path = create_log_path_variable(test_folder, simulation_file)
    timeout_call = create_timeout_function_call(SIMULATION_TIMEOUT)
    script_tag.text = log_path + simulation_script

    local_files.append(output_file)
    tree.write(output_file)

  return local_files


def main(args):
  test_name = args[1] + (" - " if len(args) > 1 else "") + str(datetime.datetime.now())
  simulation_script = ""

  with open (SCRIPT_FILE) as file:
    simulation_script = file.read()

  test_folder, simulation_folder = create_test_folder_structure(test_name)
  local_files = create_local_simulation_files(test_folder, simulation_folder)
  print("Running test suite: " + test_name + " with " + str(len(local_files)) + " test(s)")

  for file in local_files:
    path = create_local_test_folder(test_folder, file)
    print("Running test: " + os.path.basename(file) + " for " + str(SIMULATION_TIMEOUT) + " seconds... ", end="", flush=True)
    output = subprocess.run(RUN_TEST_COMMAND + [file], stdout=subprocess.PIPE, universal_newlines=True).stdout
    print("Done")
    with open(path + "/" + LOCAL_COOJA_LOG_FILE, "w") as cooja_log:
      cooja_log.write(output)


if __name__ == '__main__':
    main(sys.argv)
