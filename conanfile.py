# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class SDL2MixerConan(ConanFile):
    name = "sdl2_mixer"
    version = "2.0.4"
    description = "Keep it short"
    topics = ("conan", "sdl2_mixer", "mixer", "audio", "multimedia", "sound", "music")
    url = "https://github.com/bincrafters/conan-libname"
    homepage = "https://github.com/original_author/original_lib"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "Zlib"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "cmd": [True, False],
               "wav": [True, False],
               "flac": [True, False],
               "mpg123": [True, False],
               "ogg": [True, False],
               "opus": [True, False],
               "mikmod": [True, False],
               "modplug": [True, False],
               "nativemidi": [True, False]}
    default_options = {"shared": False,
                       "fPIC": True,
                       "cmd": False,  # needs sys/wait.h
                       "wav": True,
                       "flac": True,
                       "mpg123": True,
                       "ogg": True,
                       "opus": True,
                       "mikmod": True,
                       "modplug": True,
                       "nativemidi": True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    requires = "sdl2/2.0.9@bincrafters/stable"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def requirements(self):
        if self.options.flac:
            self.requires.add("flac/1.3.2@bincrafters/stable")
        if self.options.mpg123:
            self.requires.add("libmpg123/1.25.10@bincrafters/stable")
        if self.options.ogg:
            self.requires.add("ogg/1.3.3@bincrafters/stable")
            self.requires.add("vorbis/1.3.6@bincrafters/stable")
        if self.options.opus:
            self.requires.add("opus/1.2.1@bincrafters/stable")
            self.requires.add("opusfile/0.10@bincrafters/stable")
        if self.options.mikmod:
            self.requires.add("libmikmod/3.3.11.1@bincrafters/stable")
        if self.options.modplug:
            self.requires.add("libmodplug/0.8.9.0@bincrafters/stable")

    def source(self):
        source_url = "https://www.libsdl.org/projects/SDL_mixer/release/SDL2_mixer-%s.tar.gz" % self.version
        tools.get(source_url,
                  sha256="b4cf5a382c061cd75081cf246c2aa2f9df8db04bdda8dcdc6b6cca55bede2419")
        os.rename("SDL2_mixer-" + self.version, self._source_subfolder)

        shutil.rmtree(os.path.join(self._source_subfolder, "external"))

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["CMD"] = self.options.cmd
        cmake.definitions["WAV"] = self.options.wav
        cmake.definitions["FLAC"] = self.options.flac
        cmake.definitions["MP3_MPG123"] = self.options.mpg123
        cmake.definitions["OGG"] = self.options.ogg
        cmake.definitions["OPUS"] = self.options.opus
        # TODO : fluidsynth
        # TODO : mad (mp3)
        # TODO : tinymidy
        cmake.definitions["MOD_MIKMOD"] = self.options.mikmod
        cmake.definitions["MOD_MODPLUG"] = self.options.modplug
        cmake.definitions["MID_NATIVE"] = self.options.nativemidi

        cmake.definitions['FLAC_DYNAMIC'] = self.options['flac'].shared if self.options.flac else False
        cmake.definitions['MP3_MPG123_DYNAMIC'] = self.options['libmpg123'].shared if self.options.mpg123 else False
        cmake.definitions['OGG_DYNAMIC'] = self.options['ogg'].shared if self.options.ogg else False
        cmake.definitions['OPUS_DYNAMIC'] = self.options['opus'].shared if self.options.opus else False
        cmake.definitions['MOD_MIKMOD_DYNAMIC'] = self.options['libmikmod'].shared if self.options.mikmod else False
        cmake.definitions['MOD_MODPLUG_DYNAMIC'] = self.options['libmodplug'].shared if self.options.modplug else False

        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="COPYING.txt", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["sdl2_mixer"]
