"""Fixtures for censusgeocode."""

# This file is part of censusgeocode.
# https://github.com/fitnr/censusgeocode

# Licensed under the General Public License (version 3)
# http://opensource.org/licenses/LGPL-3.0
# Copyright (c) 2015-2026, Neil Freeman <contact@fakeisthenewreal.org>

import pytest
from censusgeocode import CensusGeocode


@pytest.fixture
def cg():
    """Provides an initialized CensusGeocode instance."""
    return CensusGeocode()


@pytest.fixture
def batch_path(request):
    """Provides either a string or a Path object for batch testing."""
    return request.param
