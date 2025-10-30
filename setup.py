#!/usr/bin/env python3
"""
GOAT Setup Script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="goat-player",
    version="1.0.0",
    author="GOAT Project",
    description="Intelligent multimedia player with AI integration and reactive visuals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Blackmvmba88/GOAT",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "Topic :: Multimedia :: Video :: Display",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pygame>=2.5.0",
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "pillow>=10.0.0",
        "librosa>=0.10.0",
        "soundfile>=0.12.0",
        "pyaudio>=0.2.13",
        "matplotlib>=3.7.0",
        "scipy>=1.11.0",
        "python-dotenv>=1.0.0",
    ],
)
