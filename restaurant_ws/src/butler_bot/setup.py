from setuptools import setup, find_packages
from glob import glob

package_name = 'butler_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', [f'resource/{package_name}']),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
        ('share/' + package_name + '/urdf', glob('urdf/*.urdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='balaji',
    maintainer_email='balaji@todo.todo',
    description='Butler robot main control package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'nav2 = butler_bot.butler_bot_nav2:main',
            'butler_bot_nav = butler_bot.butler_bot_nav:main',
            'turtle_bot = butler_bot.turtle_bot:main',
            'bot_node = butler_bot.dummy_butler_node:main',
            'load_machine_sim = butler_order_manager.load_machine_sim:main',
        ],
    },
)
