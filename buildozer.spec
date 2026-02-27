[app]
title = Arte Preco Pro Offline
package.name = arteprecooffline
package.domain = br.com.pc2026

source.dir = .
source.include_exts = py,png,jpg,kv,json

version = 1.0

requirements = python3,kivy
android.package_format = apk
orientation = portrait
fullscreen = 0

# Android
android.api = 33
android.minapi = 21
android.ndk_api = 21

# TRAVAS IMPORTANTES (evita preview e aceita licença)
android.accept_sdk_license = True
android.build_tools_version = 34.0.0
android.ndk = 25b
p4a.branch = stable

[buildozer]
log_level = 2
warn_on_root = 0
