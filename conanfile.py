from nxtools import NxConanFile
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
        self.retrieve("134bfe122fd25599bb807bb8130e7ba6d9bdb851e0b16efcb83ac4f5d0b70057",
            [
                'vendor://google/snappy/snappy-{version}.tar.gz'.format(version=self.version),
                'https://github.com/google/snappy/releases/download/{version}/snappy-{version}.tar.gz'.format(version=self.version)
            ], "snappy-{v}.tar.gz".format(v = self.version))

    def do_build(self):
        build_dir = "{staging_dir}/src".format(staging_dir=self.staging_dir)
        tools.untargz("snappy-{v}.tar.gz".format(v=self.version), build_dir)
        shared_definition = "--enable-static --disable-shared"
        if self.options.shared:
            shared_definition = "--enable-shared --disable-static"
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            self.run("cd {build_dir}/snappy-{v} && ./configure --disable-gtest prefix=\"{staging}\" {shared}".format(
                v = self.version, staging=self.staging_dir, shared=shared_definition, build_dir=build_dir))
            self.run("cd {build_dir}/snappy-{v} && make install".format(v = self.version, build_dir = build_dir))

    def do_package_info(self):
        self.cpp_info.libs = ["snappy"]

