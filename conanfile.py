#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class DateConan(ConanFile):
    version = "2.4"
    name = "date"
    license = "MIT"
    url = "https://github.com/ess-dmsc/date"
    description = "Date and time tools included the C++20 working draft"

    src_version = "2.4"
    src_url = "https://github.com/HowardHinnant/date"
    # SHA256 Checksum for this versioned release (.tar.gz)
    # NOTE: This should be updated every time the version is updated
    archive_sha256 = "549c3120fe8eaaab7f28946e2430fb0d3d4b40b843a5ea52b78dba49795c7e05"

    exports = ["LICENSE.md", "FindDate.cmake"]
    exports_sources = ["CMakeLists.txt", "date-config.cmake"]

    settings = "os", "arch", "compiler", "build_type"
    requires = (
        "libcurl/7.56.1@bincrafters/stable",
        "OpenSSL/1.0.2n@conan/stable",
        "zlib/1.2.11@conan/stable"
    )
    options = {"shared": [True, False]}

    # The folder name when the *.tar.gz release is extracted
    folder_name = name + "-%s" % src_version
    # The name of the archive that is downloaded from Github
    archive_name = "%s.tar.gz" % folder_name
    # The temporary build diirectory
    build_dir = "./%s/build" % folder_name

    default_options = (
        "shared=True",
        "libcurl:darwin_ssl=False"
    )
    generators = "cmake"

    def configure(self):
        self.requires.add("libcurl/7.56.1@bincrafters/stable", private=False)

    def source(self):
        tools.download(
            "{0}/archive/v{1}.tar.gz".format(self.src_url, self.src_version),
            self.archive_name
        )
        tools.check_sha256(
            self.archive_name,
            self.archive_sha256
        )
        tools.unzip(self.archive_name)
        os.unlink(self.archive_name)

        os.rename(os.path.join(self.folder_name, "CMakeLists.txt"),
                  os.path.join(self.folder_name, "CMakeLists_original.txt"))
        shutil.copy("CMakeLists.txt", os.path.join(self.folder_name, "CMakeLists.txt"))
        shutil.copy("date-config.cmake", os.path.join(self.folder_name, "date-config.cmake"))

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_DATE_TESTING"] = "OFF"
        cmake.configure(source_folder=self.folder_name, build_folder="build")
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE*", dst="licenses", src=self.folder_name)

        include_folder =  os.path.join(self.folder_name, "include")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)
        self.copy(pattern="date-config.cmake", dst="lib/cmake/date-"+self.version, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
