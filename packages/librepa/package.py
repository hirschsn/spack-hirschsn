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

    depends_on('cmake@3.13.0:', type='build')

    depends_on('mpi')
    depends_on('boost+serialization+mpi@1.67.0,1.68.0,1.72.0:')
    depends_on('boost+test@1.67.0,1.68.0,1.72.0:', type='test')
    depends_on('p4est-lahnerml', when='+p4est')
    depends_on('kdpart', when='+kdpart')
    depends_on('parmetis+shared', when='+parmetis')

    sanity_check_is_file = ['include/repa/repa.hpp', 'lib/librepa.so']

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DWITH_P4EST={}".format("ON" if "+p4est" in spec else "OFF"),
            "-DWITH_KDPART={}".format("ON" if "+kdpart" in spec else "OFF"),
            "-DWITH_PARMETIS={}".format("ON" if "+parmetis" in spec else "OFF"),
            "-DWITH_TESTS={}".format("ON" if self.run_tests else "OFF"),
            "-DWITH_COVERAGE=off",
        ]
        if "^openmpi" in spec and self.run_tests:
            args.append("-DMPIEXEC_PREFLAGS=--oversubscribe")
        return args

