from setuptools import setup

setup(
    name="onvif-python",
    version="0.0.1",
    description="",
    url="https://github.com/gyounghun6612/custom_onvif_python_module.git",
    author="Choi_keonghun & Jun_eins",
    author_email="dev.gyounghun6612@gmail.com",
    packages=["onvif_python"],
    zip_safe=False,
    install_requires=[
        "onvif-zeep",
        "opencv-python"
    ]
)