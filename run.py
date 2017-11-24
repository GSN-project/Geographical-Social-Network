#from setuptools import setup

#setup(
#    name='GSN',
#    packages=['GSN'],
#    include_package_data=True,
#    install_requires=[
#        'flask',
#    ],
#)
from os import environ
from GSN import create_app
app = create_app()
#app.run(debug=True)
port = int(environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)

