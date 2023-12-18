from setuptools import setup, find_packages

setup(
    name='algorithm',
    version='1.0',
    description='Quantitative algorithm',
    author='akeboshi',
    author_email='akeboshi82@gmail.com',
    packages=find_packages(),
    install_requires=[
        # List any dependencies your package requires
        'numpy<=1.24.3,>=1.22',
        'ta-lib==0.4.25',
        'requests>=2.31.0',
        'urllib3<2.0.0,>=1.25.8'
    ],
)