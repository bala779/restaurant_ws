from setuptools import setup
import os
from glob import glob

package_name = 'butler_order_manager'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'srv'), glob('srv/*.srv')),
        (os.path.join('share', package_name, 'action'), glob('action/*.action')),
        (os.path.join('share', package_name, 'reference'), glob('reference/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Balaji',
    maintainer_email='balaji@example.com',
    description='Order management for a butler robot: services for add/cancel, action-driven executor, JSON persistence.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'order_server = butler_order_manager.order_server:main',
            'order_executor = butler_order_manager.order_executor:main',
            'order_client = butler_order_manager.order_client:main',
            'order_dispatcher = butler_order_manager.order_dispatcher:main',
        ],
    },
)
