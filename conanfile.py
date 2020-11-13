import os
from conans import ConanFile, CMake, tools


class RestClientCppConan(ConanFile):
    name = "restclient-cpp"
    version = "0.5.2.eeb00a8"
    license = "MIT"
    description = "C++ client for making HTTP/REST requests"
    homepage = "http://code.mrtazz.com/restclient-cpp/"
    url = "https://github.com/igor-sadchenko/conan-restclient-cpp/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False]}
    default_options = (
        "shared=False",
        "fPIC=True",
    )
    generators = "cmake", "cmake_multi"
    exports = "LICENSE"
    exports_sources = "CMakeLists.txt", "patches/**"
    revision_mode = "scm"
    scm = {
        "type": "git",
        "subfolder": "sources",
        "url": "https://github.com/igor-sadchenko/restclient-cpp.git",
        "revision": version.split(".")[-1],
     }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def _patch_sources(self):
        tools.patch(base_path="sources", patch_file="patches/CMakeLists.txt.patch")

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        if self.settings.os == "Windows":
            if self.options.shared:
                cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = True
            cmake.definitions["CMAKE_USE_WIN32_THREADS_INIT"] = True
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("License.txt", dst="licenses", src="sources")
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["restclient-cppd" if self.settings.build_type == "Debug" else "restclient-cpp"]

    def requirements(self):
        self.requires.add('libcurl/7.68.0')
        self.requires.add('openssl/1.1.1g')