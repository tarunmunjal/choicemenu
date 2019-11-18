import setuptools

with open("README.md", "r") as fh:
    full_description = fh.read()

setuptools.setup(
    name="choicemenu-tarunmunjal",
    version="0.0.1",
    author="Tarun Munjal",
    author_email="tarunmunjal@msn.com",
    description="=A package to provide a menu for selecting from a list or dict.",
    long_description=full_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tarunmunjal/choicemenu",
    packages=setuptools.find_packages(),
    license="GPL",
    classifiers=[
        "Programming Language :: Python :: 2",
        "Operating System: OS Independent",
    ],
    python_requires=">=3.7",
)
