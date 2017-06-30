from conans import ConanFile, CMake, tools
import os


class ChaiscriptConan(ConanFile):
    name = "chaiscript"
    version = "5.8.5"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    exports = "min_max_patch.diff"

    def source(self):
        tools.download("https://github.com/ChaiScript/ChaiScript/archive/v5.8.5.tar.gz",
                       "chaiscript.tar.gz")
        tools.unzip("chaiscript.tar.gz")
        tools.replace_in_file(os.path.join("ChaiScript-5.8.5/CMakeLists.txt"), "project(chaiscript)",
                                           "project(chaiscript)\ninclude(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\nconan_basic_setup()\n")
        tools.patch("ChaiScript-5.8.5", "min_max_patch.diff", strip=1)

    def build(self):
        cmake = CMake(self)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake ChaiScript-5.8.5 -DBUILD_TESTING=OFF %s %s' % (cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.hpp", dst="include", src="ChaiScript-5.8.5/include", keep_path=True)
        self.copy("*.chai", dst="include", src="ChaiScript-5.8.5/include", keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        
        if self.options.shared:
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["chaiscript_stdlib-5.8.5"]
