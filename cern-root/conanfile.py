from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import copy, get, replace_in_file, rmdir, save, apply_conandata_patches
from conan.tools.build import check_min_cppstd
from conan.errors import ConanInvalidConfiguration


import os
import textwrap

required_conan_version = ">=2.0"


class CernRootConan(ConanFile):
    name = "cern-root"
    version = "v6-32-02"
    license = "LGPL-2.1-or-later"
    homepage = "https://root.cern/"
    url = "https://github.com/conan-io/conan-center-index"
    description = "CERN ROOT data analysis framework."
    topics = ("data-analysis", "physics")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "fPIC": [True, False],
        "python": ["off", "system"],
    }
    default_options = {
        "fPIC": True,
        "python": "off",
    }

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires("cfitsio/4.0.0")
        self.requires("fftw/3.3.9")
        self.requires("giflib/5.2.1")
        self.requires("glew/2.2.0")
        self.requires("glu/system")
        self.requires("libcurl/7.78.0")
        self.requires("libjpeg/9d")
        self.requires("libpng/1.6.37")
        self.requires("libxml2/2.9.12")
        self.requires("lz4/1.9.3")
        self.requires("opengl/system")
        self.requires("openssl/1.1.1l")
        self.requires("pcre/8.44")
        self.requires("sqlite3/3.36.0")
        self.requires("tbb/2020.3")
        self.requires("xorg/system")
        self.requires("xxhash/0.8.0")
        self.requires("xz_utils/5.2.5")
        self.requires("zstd/1.5.0")

    def validate(self):
        if self.info.options.python not in ["off", "system"]:
            raise ConanInvalidConfiguration("Invalid option for python. Use 'off' or 'system'.")
        

    def source(self):
        get(self, **self.conan_data["sources"][self.version], destination=self.source_folder, strip_root=True)
        apply_conandata_patches(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        copy(self, "LICENSE", self.source_folder, os.path.join(self.package_folder, "licenses"))
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "res"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "ROOT")
        self.cpp_info.libs = [
            "Core", "Imt", "RIO", "Net", "Hist", "Graf", "Graf3d", "Gpad", "ROOTVecOps", "Tree", "TreePlayer", "Rint",
            "Postscript", "Matrix", "Physics", "MathCore", "Thread", "MultiProc", "ROOTDataFrame"
        ]
