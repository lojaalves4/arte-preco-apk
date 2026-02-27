name: Build APK

on:
  workflow_dispatch:
  push:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install system deps
        run: |
          sudo apt update
          sudo apt install -y \
            zip unzip git openjdk-17-jdk \
            build-essential python3-pip \
            libffi-dev libssl-dev libsqlite3-dev zlib1g-dev

      - name: Install Buildozer
        run: |
          python -m pip install --upgrade pip
          pip install buildozer cython

      # Fixar versões estáveis e aceitar licenças automaticamente
      - name: Configure Buildozer
        run: |
          sed -i 's/^android\.api.*/android.api = 33/' buildozer.spec || true
          sed -i 's/^android\.minapi.*/android.minapi = 21/' buildozer.spec || true
          grep -q '^android.accept_sdk_license' buildozer.spec || echo 'android.accept_sdk_license = True' >> buildozer.spec
          grep -q '^android.sdk' buildozer.spec || true
          # Evita pegar build-tools "rc"
          grep -q '^android.build_tools_version' buildozer.spec || echo 'android.build_tools_version = 34.0.0' >> buildozer.spec

      - name: Build APK
        run: |
          buildozer -v android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: arte-preco-apk
          path: bin/*.apk
