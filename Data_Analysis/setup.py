from setuptools import setup, find_packages

setup(
    name="Data-Analysis Tools",
    version="v0.2.0",
    author="LoloCG",
    author_email="",
    description="Personal Package for multiple Data Analysis uses.",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/LoloCG/Lolos_Packages",
    # packages=find_packages(include=['', '']),
    packages=find_packages(),
    install_requires=['pandas'],
    extras_require={
        # 'excel_import_export_utils': ['pandas'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
