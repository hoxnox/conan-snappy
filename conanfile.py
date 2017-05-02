from nxtools import NxConanFile, retrieve
from conans import AutoToolsBuildEnvironment, tools
from shutil import rmtree

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
            ])

    def do_build(self):
        shared_definition = "--enable-static --disable-shared"
        if self.options.shared:
            shared_definition = "--enable-shared --disable-static"
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            self.run("cd snappy-{v} && ./configure --disable-gtest prefix=\"{staging}\" {shared}".format(
                v = self.version, staging=self.staging_dir, shared=shared_definition))
            self.run("cd snappy-{v} && make install".format(v = self.version))

    def do_package_info(self):
        self.cpp_info.libs = ["snappy"]

    def do_package(self):
        rmtree("snappy-{v}".format(v = self.version))

