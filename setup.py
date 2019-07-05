"""Setup for Genie In a Bottle"""

# Built In
from setuptools import setup, find_packages


install_requires = [
    "flask >= 1.0.3",  # Web micro framework
    "pyusb >= 1.0.2",  # Dependency for pysispm
    "pysispm >= 0.5"   # Actually controls USB Energenie devices
]


entry_points = {
    "console_scripts": ["genie_in_a_bottle=genie_in_a_bottle.main:main"]
}


setup(
    name="Genie In a Bottle",
    version="0.0.1",
    author="Jay Stringer",
    author_email="jayandrewstringer@gmail.com",
    description="REST interface for controlling USB Energenie devices",
    license=open("LICENSE.txt").read(),
    url="https://github.com/JayStringer/genie_in_a_bottle",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points=entry_points
)
