#!/usr/bin/env python3

import pytest


def pytest_addoption(parser):
    parser.addoption("--name", action="store")
    parser.addoption("--timeout", action="store")

@pytest.fixture(scope="session")
def name(request):
    name_value = request.config.option.name
    if name_value is None:
        pytest.skip("O parâmetro --name é obrigatório.")
    return name_value

@pytest.fixture(scope="session")
def timeout(request):
    timeout_value = request.config.option.timeout
    if timeout_value is None:
        timeout_value = 10000  # Valor padrão
    else:
        timeout_value = int(timeout_value)
    return timeout_value
