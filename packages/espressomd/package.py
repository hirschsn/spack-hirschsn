# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Espressomd(CMakePackage):
    """The ESPResSo package http://espressomd.org"""

    homepage = "http://espressomd.org"
    git      = "https://github.com/espressomd/espressomd.git"
    url      = "https://github.com/espressomd/espresso/releases/download/4.1.2/espresso-4.1.2.tar.gz"

    version('master', branch='python')
    version('4.1.2', sha256='00bc8e4cab8fc8f56d18978970b55f09168521ed5898a92769986f2157a81a2c')

    variant('gsl', default=False, description='Enable TODO')
    variant('hdf5', default=False, description='Enable HDF5 I/O')
    variant('features', default='lennard_jones', multi=True, values=('lennard_jones', 'collision_detection'), description='Features to enable in myconfig.hpp')

    depends_on('cmake@3.12.0:', type='build')

    depends_on('mpi')
    depends_on('boost+serialization+mpi+system+filesystem+test@1.65.0:')
    depends_on('python@3.5:')
    depends_on('py-cython')
    depends_on('py-setuptools')
    depends_on('py-numpy')
    depends_on('gsl', when='+gsl')
    depends_on('hdf5+mpi', when='+hdf5')

    def cmake_args(self):
        spec = self.spec
        return [
            "-DWITH_GSL={}".format("ON" if "+gsl" in spec else "OFF"),
            "-DWITH_HDF5={}".format("ON" if "+hdf5" in spec else "OFF"),
        ]

    @run_before('cmake')
    def generate_myconfighpp(self):
        spec = self.spec
        with open("myconfig.hpp", "w") as f:
            for val in spec.variants["features"].value:
                print("#define {}".format(val.upper()), file=f)

