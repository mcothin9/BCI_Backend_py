import subprocess
import sys
import os


def main():
    # Get the Python interpreter path
    python_executable = sys.executable

    # Set the script to run
    script_path = 'stream_player.py'

    # Conda environment activation command
    conda_activate_cmd = ". /Users/mitchell/anaconda3/bin/activate && conda activate /Users/mitchell/anaconda3/envs/bci_test"

    # For macOS
    if sys.platform == 'darwin':
        cmd = f'{conda_activate_cmd}; {python_executable} {script_path}; exit'
        subprocess.Popen(['open', '-a', 'Terminal', '-n', '--args', '-c', cmd])

    # For Linux
    elif sys.platform == 'linux':
        cmd = f'xterm -e "{conda_activate_cmd}; {python_executable} {script_path}; bash"'
        subprocess.Popen(cmd, shell=True)

    # For Windows (adapt the conda activation command for Windows)
    elif sys.platform == 'win32':
        conda_activate_cmd_windows = "<adapt conda activate command for Windows>"
        cmd = f'start cmd.exe /k "{conda_activate_cmd_windows} && {python_executable} {script_path}"'
        subprocess.Popen(cmd, shell=True)

    else:
        print('Unsupported platform:', sys.platform)


if __name__ == '__main__':
    main()
