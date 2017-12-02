#from setuptools import setup

#setup(
#    name='GSN',
#    packages=['GSN'],
#    include_package_data=True,
#    install_requires=[
#        'flask',
#    ],
#)

from GSN import create_app
app = create_app()
app.run(debug=True)
