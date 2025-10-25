from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="PySFS",
    version="1.1.0",  # 版本
    author="SFSPlayer-sys",  # 作者
    author_email="3982629860@qq.com",  # 邮箱
    description="A Python library for controlling Spaceflight Simulator through the SFSControl mod API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SFSPlayer-sys/PySFS",  # 仓库地址
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "Pillow>=9.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    license="MIT",
    keywords="spaceflight simulator sfs control api mod",
    project_urls={
        "Bug Reports": "https://github.com/SFSPlayer-sys/PySFS/issues",
        "Source": "https://github.com/SFSPlayer-sys/PySFS",
        "Documentation": "https://github.com/SFSPlayer-sys/PySFS/blob/main/README.md",
    },
)