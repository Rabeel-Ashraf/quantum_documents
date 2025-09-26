#!/bin/bash
set -o pipefail
set -ex

echo -e "\n\n\n\t\tSTART\n\n\n";

# ensure not in Quantum Documents repo folder
cd $HOME

# Check if the Quantum Documents directory already exists
if [ -d "Quantum Documents" ]; then
    echo "Quantum Documents directory exists. Updating the repository."
    cd Quantum Documents
    git stash 2>&1
    git pull 2>&1
else
    echo "Quantum Documents directory does not exist. Cloning the repository."
    git clone https://github.com/h2oai/Quantum Documents.git
    cd Quantum Documents
fi

if ! command -v conda &> /dev/null; then
    echo "Conda not found, installing Miniconda."
    wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.1.0-1-Linux-x86_64.sh
    bash ./Miniconda3-py310_23.1.0-1-Linux-x86_64.sh -b -u
    source ~/miniconda3/bin/activate
    conda init bash
    conda deactivate
else
    echo "Conda is already installed."
    source ~/miniconda3/bin/activate
    conda init bash
    conda deactivate
fi

if [ "$CONDA_DEFAULT_ENV" = "Quantum Documents" ]; then
    echo "Deactivating the Quantum Documents Conda environment."
    conda deactivate
else
    echo "The Quantum Documents Conda environment is not currently activated."
fi

echo "Installing fresh Quantum Documents env."
if conda env list | grep -q 'Quantum Documents'; then
    conda remove -n Quantum Documents --all -y
else
    echo "Quantum Documents environment does not exist."
fi
conda update conda -y
conda create -n Quantum Documents -y
conda activate Quantum Documents
conda install python=3.10 -c conda-forge -y

export CUDA_HOME=/usr/local/cuda-12.1
export PIP_EXTRA_INDEX_URL="https://download.pytorch.org/whl/cu121"
export GGML_CUDA=1
export CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_ARCHITECTURES=all"
export FORCE_CMAKE=1

# get patches
curl -O  https://h2o-release.s3.amazonaws.com/Quantum Documents/run_patches.sh
curl -O https://h2o-release.s3.amazonaws.com/Quantum Documents/trans.patch
curl -O https://h2o-release.s3.amazonaws.com/Quantum Documents/xtt.patch
curl -O https://h2o-release.s3.amazonaws.com/Quantum Documents/trans2.patch
curl -O https://h2o-release.s3.amazonaws.com/Quantum Documents/google.patch
mkdir -p docs
alias cp='cp'
cp run_patches.sh trans.patch xtt.patch trans2.patch google.patch docs/

echo "Installing fresh Quantum Documents"
set +x
export GPLOK=1
curl -fsSL https://h2o-release.s3.amazonaws.com/Quantum Documents/linux_install.sh | bash


echo -e "\n\n\n\t\t Quantum Documents installation FINISHED\n\n\n";
