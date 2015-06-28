#!/usr/bin/env python
from setuptools import setup

setup(name='pyTelegramBotAPI',
      version='0.1.7',
      description='Python Telegram bot api. ',
      author='eternnoir',
      author_email='eternnoir@gmail.com',
      url='https://github.com/eternnoir/pyTelegramBotAPI',
      packages=['telebot'],
      license='GPL2',
      keywords='tools',
      install_requires=['pytest', 'requests'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Environment :: Console',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
      ]
      )
