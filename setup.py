"""Setup for Genie In a Bottle"""

# Built In
from setuptools import setup, find_packages

# Local
from genie_in_a_bottle.version import __version__ as version


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
    version=version,
    maintainer="Jay Stringer",
    description="REST interface for controlling USB Energenie devices",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points=entry_points
)
