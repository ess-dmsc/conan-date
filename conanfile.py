#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
from conans.util import files
import shutil


class DateConan(ConanFile):
    name = "date"
    version = "2.4.2-dm1"
    description = "A date and time library based on the C++11/14/17 <chrono> header"
    url = "https://github.com/bincrafters/conan-date"
    homepage = "https://github.com/HowardHinnant/date"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "date-config.cmake"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "use_system_tz_db": [True, False], "use_tz_db_in_dot": [True, False], "disable_string_view": [True, False]}
    default_options = """
    shared=True
    fPIC=True
    use_system_tz_db=True
    use_tz_db_in_dot=False
    disable_string_view=False
    """
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        # FIXME: It's not working on Windows
        if self.settings.os == "Windows":
            raise Exception("Date is not working on Windows yet.")

    def requirements(self):
        self.requires("OpenSSL/1.0.2n@conan/stable")
        if not self.options.use_system_tz_db:
            self.requires("libcurl/7.56.1@bincrafters/stable")

    def source(self):
        #tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256="98907d243397483bd7ad889bf6c66746db0d7d2a39cc9aacc041834c40b65b98")
        #extracted_dir = self.name + "-" + self.version
        #os.rename(extracted_dir, self._source_subfolder)
        self.run(
            "git clone https://github.com/HowardHinnant/date.git"
        )
        with tools.chdir("./{}".format(self.name)):
            self.run("git checkout 54e8516af223670b75d7a17c2538c6e6d0843c1f .")
            self._source_subfolder = os.getcwd()

    def _configure_cmake(self):
        cmake = CMake(self)

        cmake.configure(source_dir=self.name, build_dir=".")
        return cmake

    def build(self):
        files.mkdir("./{}/build".format(self.name))
        shutil.copyfile(
            "conanbuildinfo.cmake",
            "./{}/build/conanbuildinfo.cmake".format(self.name)
        )
        print("HELLO" + os.getcwd())
        with tools.chdir("./{}/build".format(self.name)):
            cmake = CMake(self)
            cmake.definitions["ENABLE_DATE_TESTING"] = False
            cmake.definitions["USE_SYSTEM_TZ_DB"] = self.options.use_system_tz_db
            cmake.definitions["USE_TZ_DB_IN_DOT"] = self.options.use_tz_db_in_dot
            cmake.definitions["DISABLE_STRING_VIEW"] = self.options.disable_string_view
            cmake.configure(source_dir="..", build_dir=".")
            cmake.build(build_dir=".")

    def package(self):
        self.copy(pattern="LICENSE*", dst="licenses", src=self._source_subfolder)

        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)
        self.copy(pattern="date-config.cmake", dst="lib/cmake/date-"+self.version, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
        use_system_tz_db = 0 if self.options.use_system_tz_db else 1
        defines = ["USE_AUTOLOAD={}".format(use_system_tz_db),
                   "HAS_REMOTE_API={}".format(use_system_tz_db)]
        self.cpp_info.defines.extend(defines)
