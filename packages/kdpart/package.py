# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Kdpart(MakefilePackage):
    """Simple struct-of-arrays implementation of a k-d tree over a discrete
    domain for partitioning regular grids amongst a set of processes."""

    homepage = "https://github.com/hirschsn/kdpart"
    url      = "https://github.com/hirschsn/kdpart/archive/v1.0.1.tar.gz"

    version('1.0.1', sha256='01997e73d12af149285d3a8683d8d53eb6da053b52be1be2c7c1fec8e3c68fd0')

    depends_on('mpi')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('CXX = .*', 'CXX = ' + spec['mpi'].mpicxx)

    @property
    def build_targets(self):
        return ["libkdpart.so"]
    
    @property
    def install_targets(self):
        return ["install", "PREFIX={}".format(self.prefix)]

