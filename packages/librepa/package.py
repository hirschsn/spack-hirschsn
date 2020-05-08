# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Librepa(CMakePackage):
    """Library for load-balanced, regular grids."""

    homepage = "https://github.com/hirschsn/repa"
    git      = "https://github.com/hirschsn/repa.git"

    version('master', branch='master')

    variant('p4est', default=True, description='Enable p4est-based load-balancer')
    variant('kdpart', default=True, description='Enable kdpart-based load-balancer')
    variant('parmetis', default=True, description='Enable ParMETIS-based load-balancer')

    depends_on('cmake@3.12.0:', type='build')

    depends_on('mpi')
    # Repa currently needs boost 1.67.0 or 1.68.0
    depends_on('boost+serialization+mpi@1.67.0')
    depends_on('p4est-lahnerml', when='+p4est')
    depends_on('kdpart', when='+kdpart')
    depends_on('parmetis+shared', when='+parmetis')

    sanity_check_is_file = ['include/repa/repa.hpp', 'lib/librepa.so']

    def cmake_args(self):
        spec = self.spec
        return [
            "-DWITH_P4EST={}".format("ON" if "+p4est" in spec else "OFF"),
            "-DWITH_KDPART={}".format("ON" if "+kdpart" in spec else "OFF"),
            "-DWITH_PARMETIS={}".format("ON" if "+parmetis" in spec else "OFF"),
            "-DWITH_TESTS=on",
            "-DWITH_COVERAGE=off",
        ]

