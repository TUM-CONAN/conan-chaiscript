from conans import ConanFile, CMake, tools
import os

SHA1="be225a92099d523f05ef4c29a4c7a54f2cd951d2"

class ChaiscriptConan(ConanFile):
    name = "chaiscript"
    version = "6.0.0_2"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports = "min_max_patch.diff"
    requires = "multibuilder/1.0@hi3c/experimental"

    @property
    def package_dir(self): return "ChaiScript-{}".format(SHA1)

    def source(self):
	tools.download("https://github.com/ChaiScript/ChaiScript/archive/{}.zip".format(SHA1), "chaiscript.zip")
        tools.unzip("chaiscript.zip")
        tools.replace_in_file(os.path.join(self.package_dir, "CMakeLists.txt"), "project(chaiscript)",
                                           "project(chaiscript)\ninclude(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)\ninclude(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake OPTIONAL)\nconan_basic_setup()\n")
#        tools.patch("ChaiScript-5.8.5", "min_max_patch.diff", strip=1)

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
        cmake.configure(source_dir=os.path.join(self.conanfile_directory, self.package_dir),
                        build_dir=os.path.join(self.conanfile_directory, "build-" + arch), defs={"BUILD_TESTING": "OFF"})
        cmake.build()

    def package(self):
        self.copy("*.hpp", dst="include", src=os.path.join(self.package_dir, "include"), keep_path=True)
        self.copy("*.chai", dst="include", src=os.path.join(self.package_dir, "include"), keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", src="build-universal", keep_path=False)
        #self.copy("*.dll", dst="bin", keep_path=False)
        #self.copy("*.so", dst="lib", src="build-universal", keep_path=False)
        #self.copy("*.dylib", dst="lib", src="build-universal", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["stdlib"]
