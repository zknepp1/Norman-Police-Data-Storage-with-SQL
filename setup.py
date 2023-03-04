from setuptools import setup, find_packages

setup(
	name='project0',
	version='1.0',
	author='Zachary Knepp',
	author_email='zachary.m.knepp-1@ou.edu',
	packages=find_packages(urllib, PyPDF2,urllib.request, os, requests,bs4,
                        re, urllib.parse, sqlite3,io, numpy),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)
