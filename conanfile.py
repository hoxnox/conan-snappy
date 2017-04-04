from conans import ConanFile, ConfigureEnvironment
from conans.tools import download, untargz, check_sha256, replace_in_file
from os import unlink, chdir, getenv
from shutil import copy

vendor_dir = getenv("VENDOR_DIR", "")

class SnappyConan(ConanFile):
    name = "snappy"
    version = "1.1.4"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    url = "https://github.com/hoxnox/conan-snappy.git"
    license = "https://github.com/google/snappy/blob/master/COPYING"

    def source(self):
        tgz_name = "snappy-%s.tar.gz" % self.version;
        if len(vendor_dir) != 0:
            copy("%s/google/snappy/%s" % (vendor_dir, tgz_name), tgz_name)
        else:
            download("https://github.com/google/snappy/releases/download/%s/%s"
                    % (self.version, tgz_name), tgz_name)
        check_sha256(tgz_name, "134bfe122fd25599bb807bb8130e7ba6d9bdb851e0b16efcb83ac4f5d0b70057")
        untargz(tgz_name)
        unlink(tgz_name)

    def build(self):
       env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
       shared_definition = "--enable-static --disable-shared"
       if self.options.shared:
           shared_definition = "--enable-shared --disable-static"
       chdir("snappy-%s" % self.version)
       self.run("%s ./configure --disable-gtest prefix=\"%s/distr\" %s" % (env.command_line,
           self.conanfile_directory, shared_definition))
       self.run("%s make install" % env.command_line)

    def package(self):
        self.copy("*.h", dst="include", src="distr/include")
        self.copy("*.la"   , dst="lib", src="distr/lib")
        self.copy("*.a"    , dst="lib", src="distr/lib")
        self.copy("*.so"   , dst="lib", src="distr/lib")
        self.copy("*.dll"  , dst="lib", src="distr/lib")
        self.copy("*.dylib", dst="lib", src="distr/lib")

    def package_info(self):
        self.cpp_info.libs = ["snappy"]

    def imports(self):
        self.copy("*.dll"   , dst="bin", src="lib")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy("*.so"    , dst="lib", src="lib")


