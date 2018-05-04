#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class DateConan(ConanFile):
    name = "date"
    version = "2.4"
    description = "Date and time tools included the C++20 working draft"
    url = "https://github.com/ess-dmsc/conan-date"
    homepage = "https://github.com/HowardHinnant/date"
    license = "MIT"

    exports = ["LICENSE.md", "FindDate.cmake"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"

    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    build_requires = (
        "cmake_installer/3.10.0@conan/stable"
    )

    def source(self):
        source_url = "https://github.com/HowardHinnant/date"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_DATE_TESTING"] = "OFF"
        cmake.definitions["USE_SYSTEM_TZ_DB"] = "ON"
        cmake.configure(source_folder=self.source_subfolder, build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()
        include_folder = os.path.join(self.source_subfolder, "include")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)
        self.copy("FindDate.cmake", ".", ".")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

