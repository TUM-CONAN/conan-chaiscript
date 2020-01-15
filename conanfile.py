from conans import ConanFile, CMake, tools
import os

class ChaiscriptConan(ConanFile):
    name = "chaiscript"
    version = "6.1.0"
    license = "<Put the package license here>"
    url = "https://github.com/TUM-CONAN/conan-chaiscript"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    _source_dir = "ChaiScript-{}".format(version)

    def source(self):
        tools.download("https://github.com/ChaiScript/ChaiScript/archive/v{}.zip".format(self.version), "chaiscript.zip")
        tools.unzip("chaiscript.zip")
        tools.replace_in_file(os.path.join(self._source_dir, "CMakeLists.txt"), "project(chaiscript)",
                                           """project(chaiscript)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup() """)

    def _cmake_configure(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTING"] = "OFF"
        cmake.configure(source_dir=self._source_dir)
        return cmake


    def build(self):
        cmake = self._cmake_configure()
        cmake.build()

    def package(self):
        cmake = self._cmake_configure()
        cmake.install()

    # def package(self):
    #     self.copy("*.hpp", dst="include", src=os.path.join(self.package_dir, "include"), keep_path=True)
    #     self.copy("*.chai", dst="include", src=os.path.join(self.package_dir, "include"), keep_path=True)
    #     self.copy("*.lib", dst="lib", keep_path=False)
    #     self.copy("*.a", dst="lib", src="build-universal", keep_path=False)
        #self.copy("*.dll", dst="bin", keep_path=False)
        #self.copy("*.so", dst="lib", src="build-universal", keep_path=False)
        #self.copy("*.dylib", dst="lib", src="build-universal", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
