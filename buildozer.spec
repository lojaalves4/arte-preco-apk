[app]
title = Arte Preco Pro Offline
package.name = arteprecooffline
package.domain = br.com.pc2026

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,txt,json,db

version = 1.0

requirements = python3,kivy,requests,urllib3,idna,chardet,certifi,sqlite3

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[android]
android.api = 33
android.minapi = 21

# ESSENCIAL: fixa build-tools estável (sem RC)
android.build_tools_version = 33.0.2

# NDK estável compatível com p4a/buildozer
android.ndk = 25b

android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True
