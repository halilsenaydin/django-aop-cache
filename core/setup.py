from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="core",
    version="1.0.0",
    description="Reusable core components for Django-based projects and microservices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Halil İbrahim ŞENAYDIN",
    author_email="halilsenaydin@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=4.2.7",
        "djangorestframework>=3.14.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
