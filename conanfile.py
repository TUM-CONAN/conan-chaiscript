from conans import ConanFile, CMake, tools
import os


class ChaiscriptConan(ConanFile):
    name = "chaiscript"
    version = "5.8.5_1"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports = "min_max_patch.diff"
    requires = "multibuilder/1.0@hi3c/experimental"

    def source(self):
        tools.download("https://github.com/ChaiScript/ChaiScript/archive/v5.8.5.tar.gz",
                       "chaiscript.tar.gz")
        tools.unzip("chaiscript.tar.gz")
        tools.replace_in_file(os.path.join("ChaiScript-5.8.5/CMakeLists.txt"), "project(chaiscript)",
                                           "project(chaiscript)\ninclude(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)\ninclude(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake OPTIONAL)\nconan_basic_setup()\n")
        tools.patch("ChaiScript-5.8.5", "min_max_patch.diff", strip=1)

    def build(self):
        if self.settings.arch == "universal":
            with tools.pythonpath(self):
                from multibuilder import MultiBuilder
                self.builder = MultiBuilder(self, ("armv7", "arm64", "x86_64", "i386"))
                self.builder.multi_build(self.real_build)
                return
        self.real_build(str(self.settings.arch), "")
                

    def real_build(self, arch, triple):
        cmake = CMake(self)
        cmake.configure(source_dir=os.path.join(self.conanfile_directory, "ChaiScript-5.8.5"),
                        build_dir=os.path.join(self.conanfile_directory, "build-" + arch), defs={"BUILD_TESTING": "OFF"})
        cmake.build()

    def package(self):
        self.copy("*.hpp", dst="include", src="ChaiScript-5.8.5/include", keep_path=True)
        self.copy("*.chai", dst="include", src="ChaiScript-5.8.5/include", keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", src="build-universal", keep_path=False)
        self.copy("*.dylib", dst="lib", src="build-universal", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["chaiscript_stdlib-5.8.5"]
