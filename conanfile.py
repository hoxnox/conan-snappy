from nxtools import NxConanFile, retrieve
from conans import AutoToolsBuildEnvironment, tools
from os import chdir

class SnappyConan(NxConanFile):
    name = "snappy"
    description = "Snappy, a fast compressor/decompressor."
    version = "1.1.4"
    options = {"shared":[True, False]}
    default_options = "shared=False"
    url = "https://github.com/hoxnox/conan-snappy.git"
    license = "https://github.com/google/snappy/blob/master/COPYING"

    def do_source(self):
        retrieve("134bfe122fd25599bb807bb8130e7ba6d9bdb851e0b16efcb83ac4f5d0b70057",
            [
                'vendor://google/snappy/snappy-{version}.tar.gz'.format(version=self.version),
                'https://github.com/google/snappy/releases/download/{version}/snappy-{version}.tar.gz'.format(version=self.version)
            ],
            'snappy-{version}.tar.gz'.format(version=self.version))

    def do_build(self):
        shared_definition = "--enable-static --disable-shared"
        if self.options.shared:
            shared_definition = "--enable-shared --disable-static"
        chdir("snappy-%s" % self.version)
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            self.run("./configure --disable-gtest prefix=\"%s/distr\" %s" % (
                self.conanfile_directory, shared_definition))
            self.run("make install")

    def do_package_info(self):
        self.cpp_info.libs = ["snappy"]

