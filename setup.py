from setuptools import setup
from flask_tor import __version__

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="flask-tor",
    version=__version__,
    author="Jak Bin",
    description="A simple way to run Flask apps on tor from your machine.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/jakbin/flask-tor",
    project_urls={
    'Bug Tracker': 'https://github.com/jakbin/flask-tor/issues',
    },
    license="MIT License",
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='flask, tor,onion',
    python_requires=">=3",
    packages=['flask_tor'],
    package_data={  
        'flask_tor': [
            'torrc_template',
            'torrc_template-windows'
        ]},
    install_requires=['Flask','stem'],
    zip_safe=False,
)
