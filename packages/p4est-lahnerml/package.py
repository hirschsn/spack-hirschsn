# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class P4estLahnerml(AutotoolsPackage):
    """Michael Lahnert's p4est version."""

    homepage = "https://github.com/lahnerml/p4est"
    #url      = "https://github.com/hirschsn/p4est/blob/p4est-ESPResSo-integration/dist/p4est-1.1.871-380e.tar.gz?raw=true"
    git      = "https://github.com/lahnerml/p4est"

    #version('1.1.871-380e', sha256='14085309eb8c78c6e4eec392696c343292bd17b3248cb8c6978b21c22b5a9d9f')
    version('master', branch='p4est-ESPResSo-integration', submodules=True)

    variant('openmp', default=False, description='Enable OpenMP')
    variant('blas', default=True, description='Enable BLAS')
    variant('lapack', default=True, description='Enable Lapack')

    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool@2.4.2', type='build')

    depends_on('mpi')
    depends_on('zlib')
    depends_on('blas', when='+blas')
    depends_on('lapack', when='+lapack')


    def autoreconf(self, spec, prefix):
        bootstrap = Executable('./bootstrap')
        bootstrap()

    def configure_args(self):
        args = [
            '--enable-mpi',
            '--enable-shared',
            '--enable-silent-rules',
            'CPPFLAGS=-DSC_LOG_PRIORITY=SC_LP_ESSENTIAL',
            'CFLAGS=-O2',
            'CC=%s'  % self.spec['mpi'].mpicc,
            'CXX=%s' % self.spec['mpi'].mpicxx,
            'FC=%s'  % self.spec['mpi'].mpifc,
            'F77=%s' % self.spec['mpi'].mpif77
        ]

        if '+openmp' in self.spec:
            try:
                args.append(
                    '--enable-openmp={0}'.format(self.compiler.openmp_flag))
            except UnsupportedCompilerFlag:
                args.append('--enable-openmp')
        else:
            args.append('--disable-openmp')

        if '+blas' in self.spec:
            args.append('--with-blas')
            args.append('BLAS_LIBS={}'.format(self.spec['blas'].libs.ld_flags))
        else:
            args.append('--without-blas')

        if '+lapack' in self.spec:
            args.append('--with-lapack')
            args.append('LAPACK_LIBS={}'.format(self.spec['lapack'].libs.ld_flags))
        else:
            args.append('--without-lapack')

        return args

