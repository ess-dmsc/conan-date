#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.model.version import Version
from conans.errors import ConanInvalidConfiguration
import os


class DateConan(ConanFile):
    name = "date"
    version = "aaaaaaa"
    description = "A date and time library based on the C++11/14/17 <chrono> header"
    url = "https://github.com/ess-dmsc/conan-date"
    homepage = "https://github.com/HowardHinnant/date"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "date-config.cmake"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "use_system_tz_db": [True, False],
               "use_tz_db_in_dot": [True, False]}
    default_options = {"shared": False, "fPIC": True, "use_system_tz_db": True, "use_tz_db_in_dot": False}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")
            self.options.remove("use_system_tz_db")
            self.options.remove("use_tz_db_in_dot")
        if self.settings.os == "Macos":
            self.options["libcurl"].darwin_ssl = False

    def configure(self):
        # FIXME: It's not working on Windows
        if self.settings.os == "Windows":
            raise Exception("Date is not working on Windows yet.")

        compiler_version = Version(self.settings.compiler.version.value)
        if self.settings.compiler == "Visual Studio" and compiler_version < "14":
            raise ConanInvalidConfiguration("date requires Visual Studio 2015 and higher")
        if self.settings.compiler == "apple-clang" and compiler_version < "8.0":
            raise ConanInvalidConfiguration("date requires Apple Clang 8 and higher")

    def requirements(self):
        self.requires("libcurl/7.71.0")

    def source(self):
        self.run("git clone https://github.com/HowardHinnant/date.git " + self._source_subfolder)

        with tools.chdir(self._source_subfolder):
            self.run("git checkout " + self.version + " .")
            
        tools.replace_in_file(os.path.join(self._source_subfolder, 'CMakeLists.txt'),
                              '${CURL_LIBRARIES}', '${CONAN_LIBS}')

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_DATE_TESTING"] = False
        if self.settings.os == "Windows":
            cmake.definitions["USE_TZ_DB_IN_DOT"] = False
            cmake.definitions["USE_SYSTEM_TZ_DB"] = False
        else:
            cmake.definitions["USE_TZ_DB_IN_DOT"] = self.options.use_tz_db_in_dot
            cmake.definitions["USE_SYSTEM_TZ_DB"] = self.options.use_system_tz_db
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE.txt", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        self.copy(
            pattern="date-config.cmake",
            dst="lib/cmake/date-" + self.version,
            keep_path=False,
        )

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
        if self.settings.os == "Windows":
            use_system_tz_db = 0
        else:
            use_system_tz_db = 0 if self.options.use_system_tz_db else 1
        defines = ["USE_AUTOLOAD={}".format(use_system_tz_db),
                   "HAS_REMOTE_API={}".format(use_system_tz_db)]
        self.cpp_info.defines.extend(defines)
