from setuptools import setup
setup(
    name='telediscordbot',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'telediscordbot=bot:post_handler'
        ]
    }, install_requires=['telebot', 'requests', 'dhooks', 'Pillow']
)