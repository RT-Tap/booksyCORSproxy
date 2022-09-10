from setuptools import setup

setup(
    name='booksyAPI',
    version='1.0',
    packages=['booksyAPI'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['requests', 'Flask[async]', 'flask_cors', 'flask_api', 'waitress'] 
)

# how we package up 
# /yourapplication
#     setup.py
#     /yourapplication
#         __init__.py
#         views.py
#         /static
#             style.css
#         /templates
#             layout.html
#             index.html
#             login.html
#             ...
# develiopment: 
# linux: 
#   export FLASK_APP=booksyAPI  
#   export FLASK_ENV=development
# windows:
#   $env:FLASK_APP = "booksyAPI"
#   $env:FLASK_ENV = "development"
# (ana)conda
#   conda env config vars set FLASK_APP='booksyAPI:app'
#   conda env config vars set FLASK_ENV='booksyAPI:app' 
# cd to first layer /yourapplication where setup.py resides
# pip install -e .
# flask run
#
# production 
# linux:
#   export FLASK_ENV=production 
# windows: 
#   $env:FLASK_ENV = "production"
# (ana)conda:
#   conda env config vars set FLASK_ENV='production' 
# cd to first layer /yourapplication where setup.py resides
# python setup.py bdist_wheel   
# take wheel file (./dist/ApplicationName-x-py3-none-any.whl) and put it into wherever you want to install
# pip install ApplicationName-x-py3-none-any.whl
#
#  sources/info
# https://flask.palletsprojects.com/en/2.1.x/patterns/distribute/
# https://flask.palletsprojects.com/en/2.1.x/patterns/packages/
# https://flask.palletsprojects.com/en/2.1.x/tutorial/deploy/ 
# https://flask.palletsprojects.com/en/2.1.x/deploying/
# https://flask.palletsprojects.com/en/2.1.x/deploying/waitress/
# https://stackoverflow.com/questions/70321014/runtimeerror-install-flask-with-the-async-extra-in-order-to-use-async-views
# alternate/update: https://flask.palletsprojects.com/en/2.1.x/deploying/gunicorn/