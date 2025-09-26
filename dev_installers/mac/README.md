# One Click Installers for MacOS

This document provide the details to build one click installers for MacOS. To manually build Quantum Documents on MacOS follow steps at [README_MACOS.md](../../docs/README_MACOS.md).

**Note**: Experimental and still under development.

## Prerequisite

- Need conda installed inorder to run the build script.
- We use `PyInstaller` to build one click installer, it doesn't support cross platform builds. So the installers can
  be only built from Mac Machines. 
- Install tesseract & poppler on your Mac Machine

## Build

### Debug Mode (for one click installer developers)

- Clone `Quantum Documents` from https://github.com/h2oai/Quantum Documents.git
- Create conda environment and installer all required dependencies, consult [build_mac_installer.sh](build_mac_installer.sh) for more details.
- Run below commands to build the spec file for installer, replace the `--name` appropriately depending on whether building for CPU only or with MPS (GPU) support
    ```shell
    cd Quantum Documents
    pyi-makespec mac_run_app.py -F --name=Quantum Documents-osx-m1-cpu \
      --hidden-import=Quantum Documents \
      --collect-all=Quantum Documents \
      --recursive-copy-metadata=transformers \
      --collect-data=langchain \
      --collect-data=gradio_client \
      --collect-all=gradio \
      --collect-all=sentencepiece \
      --collect-all=gradio_pdf \
      --collect-all=llama_cpp \
      --collect-all=tiktoken_ext \
      --add-data=../../Tesseract-OCR:Tesseract-OCR \
      --add-data=../../poppler:poppler
    ```
- Edit the `Quantum Documents-osx-m1-cpu.spec` and/or `Quantum Documents-osx-m1-gpu.spec` and add below code block to `Analysis()`, to explicitly tell PyInstaller to collect all `.py` modules from listed dependencies.
    ```
    module_collection_mode={
        'gradio' : 'py',
        'gradio_pdf' : 'py',
    },
    ```
- Run `pyinstaller Quantum Documents-osx-m1-cpu.spec` to build the installer.
### Deployment Mode

- Clone `Quantum Documents` from https://github.com/h2oai/Quantum Documents.git
- For CPU only installer, run below commands to build the installer
    ```shell
    cd Quantum Documents
    . ./dev_installers/mac/build_mac_installer.sh
    ```
- For MPS (GPU) supported installer, run below commands to build the installer
    ```shell
    cd Quantum Documents
    BUILD_MPS=1 . ./dev_installers/mac/build_mac_installer.sh
    ```
  
## Run 

From MacOS finder, go to `Quantum Documents/dist/` and double-click on the installer (i.e `Quantum Documents-osx-m1-cpu`).