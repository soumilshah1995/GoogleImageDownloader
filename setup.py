from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="googleimagedownloader",
    version="4.0.0",
    description="""
        Download any Image from Google Search with 2 lines of Python code     
     """,
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/soumilshah1995/GoogleImageDownloader",
    author="Soumil Nitin Shah",
    author_email="soushah@my.bridgeport.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["googleimagedownloader"],
    include_package_data=True,
    install_requires=["requests-futures", "pandas", "bs4", "requests"]
)