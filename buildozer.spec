[app]
title = Arte Preco Pro Offline
package.name = arteprecooffline
package.domain = br.com.pc2026

source.dir = .
source.include_exts = py,png,jpg,kv,json

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 21
android.ndk_api = 21

# ✅ MUITO IMPORTANTE: aceitar licença automaticamente
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0

Depois Commit changes.

2) Ajuste do .github/workflows/main.yml (APAGA e COLA)

Abra .github/workflows/main.yml e substitua por isto:

name: Build APK

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install system deps
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            zip unzip git \
            openjdk-17-jdk \
            build-essential \
            libffi-dev libssl-dev \
            zlib1g-dev \
            libncurses5

      - name: Install Buildozer
        run: |
          python -m pip install --upgrade pip
          pip install buildozer==1.5.0 Cython==0.29.36

      # ✅ Aceitar licenças do Android SDK (o que está te travando)
      - name: Accept Android SDK licenses
        run: |
          mkdir -p "$HOME/.android"
          touch "$HOME/.android/repositories.cfg"
          yes | sdkmanager --licenses || true

      - name: Build APK
        run: |
          buildozer -v android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: arte-preco-apk
          path: |
            bin/*.apk
            bin/*.aab
