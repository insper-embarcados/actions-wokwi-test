import pytest
import os
import shutil
import subprocess

import toml

test_folder = ".test"


def copy_files(exe_name):
    shutil.copyfile(f"{exe_name}/diagram.json", f"{test_folder}/diagram.json")
    shutil.copyfile(f"{exe_name}/test.yaml", f"{test_folder}/test.yaml")


def gen_wokwi_toml(exe_name):
    base_path = os.path.join("..", "build", exe_name)
    firmware_path = os.path.join(base_path, f"{exe_name}.uf2")
    elf_path = os.path.join(base_path, f"{exe_name}.elf")

    data = {"wokwi": {"version": 1, "firmware": firmware_path, "elf": elf_path}}
    os.makedirs(test_folder, exist_ok=True)
    toml_file_path = os.path.join(test_folder, "wokwi.toml")
    with open(toml_file_path, "w") as toml_file:
        toml.dump(data, toml_file)


def run_command(command, cwd=None):
    print(f"$ {command}")
    result = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")

    if result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {command}")


def run_build(name):
    firmware = os.path.join("build", name, f"{name}.uf2")
    elf = os.path.join("build", name, f"{name}.elf")
    missing = [path for path in (firmware, elf) if not os.path.isfile(path)]

    if missing:
        raise RuntimeError(
            "Build artifacts not found. Run insper-embarcados/pico-build before "
            f"actions-wokwi-test. Missing: {', '.join(missing)}"
        )

    print(f"Using existing firmware: {firmware}")
    print(f"Using existing ELF: {elf}")


def run_test(name, timeout):
    print("Checking build artifacts")
    run_build(name)
    gen_wokwi_toml(name)
    copy_files(name)

    print("Running Wokwi scenario")
    run_command(f"wokwi-cli --timeout {timeout} --scenario test.yaml", cwd=test_folder)
    return 0


def test_code(name, timeout):
    assert run_test(name, timeout) == 0
