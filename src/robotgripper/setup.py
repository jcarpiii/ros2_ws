from setuptools import setup
from glob import glob
import os

package_name = "robotgripper"


def package_tree(src_dir):
    """
    Return a list of (destination, [files]) tuples that recreates
    the full folder hierarchy of *src_dir* inside
    share/<package_name>/<src_dir>/…
    """
    data = []
    for path in glob(os.path.join(src_dir, "**", "*"), recursive=True):
        if os.path.isfile(path):
            rel_path = os.path.relpath(path, src_dir)          # e.g. ur10e/visual/base.dae
            dest = os.path.join("share", package_name, src_dir, os.path.dirname(rel_path))
            data.append((dest, [path]))
    return data


data_files = [
    # make the package discoverable by ament
    ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
    ("share/" + package_name, ["package.xml"]),

    # plain folders (flat copy)
    ("share/" + package_name + "/launch", glob("launch/*.py")),
    ("share/" + package_name + "/urdf",   glob("urdf/*")),
    ("share/" + package_name + "/config", glob("config/*")),
]

# preserve full sub‑tree for meshes (visual/ & collision/)
data_files += package_tree("meshes")
data_files += package_tree("urdf")

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],          # keep if you have a python module; else []
    data_files=data_files,
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Jack Carpenter",
    maintainer_email="jack@example.com",
    description="UR10e + gripper meshes and URDFs",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            # add python executables here if you create any
        ],
    },
)
