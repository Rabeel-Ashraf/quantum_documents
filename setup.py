import os
import setuptools
from typing import List
from setuptools import find_packages

for_pypi = os.getenv('PYPI') is not None


def parse_requirements(file_name: str) -> List[str]:
    if not os.path.exists(file_name):
        return []
    with open(file_name) as f:
        lines = f.read().splitlines()
    lines = [line for line in lines if line.strip() and not line.strip().startswith("#")]
    requirements = []
    for line in lines:
        if 'chromamigdb' in line:
            continue
        if for_pypi:
            if 'http://' in line or 'https://' in line:
                continue
            if 'llama-cpp-python' in line and ';' in line:
                line = line[:line.index(';')]
        requirements.append(line)
    return requirements


install_requires = parse_requirements('requirements.txt')

req_files = [
    'reqs_optional/requirements_optional_langchain.txt',
    'reqs_optional/requirements_optional_llamacpp_gpt4all.txt',
    'reqs_optional/requirements_optional_langchain.gpllike.txt',
    'reqs_optional/requirements_optional_agents.txt',
    'reqs_optional/requirements_optional_langchain.urls.txt',
    'reqs_optional/requirements_optional_doctr.txt',
    'reqs_optional/requirements_optional_audio.txt',
    'reqs_optional/requirements_optional_image.txt',
]

for req_file in req_files:
    install_requires.extend(parse_requirements(req_file))

install_cpu = parse_requirements('reqs_optional/requirements_optional_cpu_only.txt')
install_cuda = parse_requirements('reqs_optional/requirements_optional_gpu_only.txt')
install_extra_training = parse_requirements('reqs_optional/requirements_optional_training.txt')
install_wiki_extra = parse_requirements('reqs_optional/requirements_optional_wikiprocessing.txt')

current_directory = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(current_directory, 'version.txt'), encoding='utf-8') as f:
    version = f.read().strip()

# ✅ CORRECT: Use 'quantum_docs' (the actual folder name)
packages = find_packages(include=['quantum_docs*'], exclude=['tests*'])

setuptools.setup(
    name='quantum-documents',  # ← PyPI/human-readable name (hyphen OK)
    version=version,
    license='Apache-2.0',  # ← SPDX identifier
    description='Quantum Documents: Advanced AI-powered document processing and RAG platform',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name or Organization',
    author_email='your.email@example.com',
    url='https://github.com/your-username/quantum-documents',
    keywords=['LLM', 'AI', 'RAG', 'Document AI'],
    packages=packages,
    package_data={
        'quantum_docs': ['spkemb/*.npy'],
    },
    exclude_package_data={
        'quantum_docs': [
            '**/__pycache__/**',
            'models/README-template.md'
        ],
    },
    install_requires=install_requires,
    extras_require={
        'cpu': install_cpu,
        'cuda': install_cuda,
        'training': install_extra_training,
        'wiki': install_wiki_extra,
        'local-inference': ['unstructured[local-inference]>=0.12.5,<0.13'],
    },
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'quantum-docs-finetune=quantum_docs.finetune:entrypoint_main',
            'quantum-docs-generate=quantum_docs.generate:entrypoint_main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)