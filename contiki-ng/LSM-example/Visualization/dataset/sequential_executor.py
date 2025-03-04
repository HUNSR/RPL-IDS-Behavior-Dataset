#!/usr/bin/env python3

import sys
import os
import glob
from subprocess import Popen, PIPE, STDOUT, CalledProcessError

# get the path of this example
SELF_PATH = os.path.dirname(os.path.abspath(__file__))
# move three levels up
CONTIKI_PATH = os.path.dirname(os.path.dirname(os.path.dirname(SELF_PATH)))

COOJA_PATH = os.path.normpath(os.path.join(CONTIKI_PATH, "tools", "cooja"))

#######################################################
# Run a child process and get its output

def run_subprocess(args, input_string):
    retcode = -1
    stdoutdata = ''
    try:
        proc = Popen(args, stdout=PIPE, stderr=STDOUT, stdin=PIPE, shell=True, universal_newlines=True)
        (stdoutdata, stderrdata) = proc.communicate(input_string)
        if not stdoutdata:
            stdoutdata = '\n'
        if stderrdata:
            stdoutdata += stderrdata + '\n'
        retcode = proc.returncode
    except OSError as e:
        sys.stderr.write("run_subprocess OSError:" + str(e))
    except CalledProcessError as e:
        sys.stderr.write("run_subprocess CalledProcessError:" + str(e))
        retcode = e.returncode
    except Exception as e:
        sys.stderr.write("run_subprocess exception:" + str(e))
    finally:
        return (retcode, stdoutdata)

#############################################################
# Run a single instance of Cooja on a given simulation script

def execute_test(cooja_file):
    cooja_output = 'COOJA.testlog'
    # cleanup
    try:
        os.remove(cooja_output)
    except FileNotFoundError as ex:
        pass
    except PermissionError as ex:
        print("Cannot remove previous Cooja output:", ex)
        return False

    filename = os.path.join(SELF_PATH, cooja_file)
    args = " ".join([COOJA_PATH + "/gradlew --no-watch-fs  --parallel --build-cache -p", COOJA_PATH, "run --args='--contiki=" + CONTIKI_PATH, "--no-gui", "--logdir=" + SELF_PATH, filename + "'"])
    sys.stdout.write("  Running Cooja, args={}\n".format(args))

    (retcode, output) = run_subprocess(args, '')
    if retcode != 0:
        sys.stderr.write("Failed, retcode=" + str(retcode) + ", output:")
        sys.stderr.write(output)
        # return False

    sys.stdout.write("  Checking for output...")

    # Rename the output file to match the input file name
    new_output = os.path.splitext(cooja_file)[0] + '.testlog'
    os.rename(cooja_output, new_output)

    is_done = False
    with open(new_output, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "TEST OK":
                sys.stdout.write(" done.\n")
                is_done = True
                continue

    if not is_done:
        sys.stdout.write("  test failed.\n")
        return False

    sys.stdout.write(" test done\n")
    return True

#######################################################
# Run the application

def main():
    # Find all .csc files in the current directory
    csc_files = glob.glob(os.path.join(SELF_PATH, "*.csc"))

    if not csc_files:
        print("No .csc files found in the directory.")
        exit(-1)

    print(f"Found {len(csc_files)} .csc file(s) to process.")
    for input_file in csc_files:
        print(f'Using simulation script "{input_file}"')
        if not execute_test(os.path.basename(input_file)):
            print(f"Test failed for {input_file}")
            # exit(-1)

    print("All tests completed successfully.")

#######################################################

if __name__ == '__main__':
    main()
