# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class A(AutotoolsPackage):
    """Simple package to test ABI variants."""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef', abi='changed')
    version('1.0.1', '9876543210fedcba9876543210fedcba', abi='equivalent', abi_base='1.0')
    version('1.0.2', 'fedcba987654310fedcba987654310', abi='additive', abi_base='1.0')
    version('2.0', 'abcdef0123456789abcdef0123456789', abi='changed')
    version('3.0', '1234abcdef0123456789abcdef012345', abi='subtractive', abi_base='2.0')

    variant(
        'foo', description='',
        values=any_combination_of('bar', 'baz', 'fee').with_default('bar')
    )

    variant(
        'foobar',
        values=('bar', 'baz', 'fee'),
        default='bar',
        description='',
        multi=False,
        abi='equivalent'
    )

    # Default for booleans: changed
    variant('lorem_ipsum', description='', default=False, abi='additive')

    # 
    variant('bvv', values=(Value(0, abistuff), 1, 2), default=0, description='The good old BV variant',
            abi={0: 'equivalent',
                 1: 'additive',
                 2: 'changed'})

    variant('bvv', values=(0, 1, 2), default=0, description='The good old BV variant',
            when='@3.0:', abi='additive')

    depends_on('b', when='foobar=bar', abi_hidden=True)  # This hides ABI.
    depends_on('test-dependency', type='test')

    # Link and run dependencies are relevant to abi compatibility for this
    # package.
    abi_deptypes(('link', 'run'))

    # None of the platform, os, arch tuple matters for this package.
    abi_arch = False

    parallel = False

    def autoreconf(self, spec, prefix):
        pass

    def configure(self, spec, prefix):
        pass

    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        # sanity_check_prefix requires something in the install directory
        # Test requires overriding the one provided by `AutotoolsPackage`
        mkdirp(prefix.bin)
