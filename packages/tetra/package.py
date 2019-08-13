# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tetra(MakefilePackage):
    """Simple CGAL-based 3D inside-polygon test."""

    homepage = "https://github.com/hirschsn/tetra"
    url      = "https://github.com/hirschsn/tetra/archive/v1.0.0.tar.gz"

    version('1.0.0', sha256='918daf8bcf3946a5406317017c94cb56d0f35deb217cdbcde1ebc5bb600d321b')

    depends_on('cgal')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('CXX = .*', 'CXX = ' + env['CXX'])

    @property
    def build_targets(self):
        return ["libtetra.so"]
    
    @property
    def install_targets(self):
        return ["install", "PREFIX={}".format(self.prefix)]


