from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="PySFS",
    version="1.0.0",  # 版本信息
    author="SFSGamer",  # 作者信息
    author_email="",  # 可根据实际情况补充作者邮箱
    description="A Python library for controlling Spaceflight Simulator through the SFSControl mod API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SFSPlayer-sys/PySFS",  # 更新为项目实际仓库地址
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",  # 与requirements.txt保持一致
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",  # MIT开源协议
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    license="MIT",  # 明确指定许可证
)