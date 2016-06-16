from conans import ConanFile, ConfigureEnvironment
from conans.tools import download, untargz, check_sha256
from os import unlink,chdir
from shutil import copy

class SnappyConan(ConanFile):
    name = "snappy"
    version = "1.1.3"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def source(self):
        zip_name = "snappy-1.1.3.zip";
        #download("https://github.com/google/snappy/releases/download/1.1.3/snappy-1.1.3.tar.gz", zip_name)
        copy("/home/hoxnox/Downloads//snappy-1.1.3.tar.gz", zip_name)
        check_sha256(zip_name, "f94c0f816510a95d7521c725e9ddf48bfd600a0f6623d33c9a6a92ec824d8c12")
        untargz(zip_name)
        unlink(zip_name)

    def build(self):
       env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
       shared_definition = "--enable-static --disable-shared"
       if self.options.shared:
           shared_definition = "--enable-shared --disable-static"
       chdir("snappy-1.1.3")
       self.run("%s ./autogen.sh" % (env.command_line))
       self.run("%s ./configure %s" % (env.command_line, shared_definition))
       self.run("%s make" % env.command_line)

    def package(self):
        self.copy("*.h", dst="include")
        self.copy("*.lib", dst="lib", src="lib")
        self.copy("*.a", dst="lib", src="lib")

    def package_info(self):
        self.cpp_info.libs = ["snappy"]

    def imports(self):
       self.copy("*.dll", dst="bin", src="bin")
       self.copy("*.dylib*", dst="bin", src="lib")
       self.copy("*.so", dst="bin", src="lib")


