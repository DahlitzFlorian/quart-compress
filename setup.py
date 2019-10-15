import setuptools

setuptools.setup(
    name='Quart-Compress',
    version='1.0.0',
    url='https://github.com/DahlitzFlorian/quart-compress',
    license='MIT',
    author='Florian Dahlitz',
    author_email='f2dahlitz@freenet.de',
    description='Compress responses in your Quart app with gzip.',
    long_description='Full documentation can be found on the Quart-Compress "Home Page".',
    py_modules=['quart_compress'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Quart'
    ],
    test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
