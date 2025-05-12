import pytest
import subprocess
import os

def run_build(name):
    if not os.path.isdir("build"):
        os.makedirs("build", exist_ok=True)
        os.chdir("build")
        subprocess.run(
            "cmake ..",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    else:
        os.chdir("build")
        
    subprocess.run(
        f"make {name}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    os.chdir("..")


def test_code(name):
    print("Building projects")
    run_build(name)
    command = f"wokwi-cli --timeout 10000 --scenario test.yaml {name}"
    process = subprocess.run(command, shell=True, stderr=subprocess.PIPE, text=True)
    assert process.returncode == 0

