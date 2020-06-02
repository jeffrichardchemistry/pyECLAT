from setuptools import setup, find_packages

with open("README.md", 'r') as fr:
	description = fr.read()

setup(
    name='pyECLAT',
    version='1.0.0',
    url='https://github.com/jeffrichardchemistry/pyECLAT',
    license='BSD License',
    author='Jefferson Richard',
    author_email='jrichardquimica@gmail.com',
    keywords='Data Science ECLAT Association statistic Artificial intelligence',
    description='A package for association analysis using the ECLAT method.',
    long_description = description,
    long_description_content_type = "text/markdown",
	#data_files=[('pyECLAT',['data/base1.csv', 'data/base2.csv'])],
	package_data={'data':['base1.csv', 'base2.csv']},
    packages=['pyECLAT'],
    install_requires=['pandas>=0.25.3', 'numpy>=1.17.4', 'tqdm>=4.41.1'],
	classifiers = [
		'Intended Audience :: Developers',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: BSD License',
		'Natural Language :: English',
		'Operating System :: Unix',
		'Operating System :: Linux',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: MacOS',
		'Topic :: Scientific/Engineering :: Artificial Intelligence',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6']
)
