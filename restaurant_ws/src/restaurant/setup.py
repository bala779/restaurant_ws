from setuptools import find_packages, setup
import glob
import os

package_name = 'restaurant'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob.glob('launch/restaurant.launch.py')),
        ('share/' + package_name + '/urdf', glob.glob('urdf/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='balaji',
    maintainer_email='balaji@todo.todo',
    description='Launch package for restaurant simulation',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)
