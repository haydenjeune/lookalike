resources(
  name='api-config',
  sources=['spec.yaml'],
)

python_library(
  dependencies=[
    '3rdparty/python:connexion',
    '3rdparty/python:pillow',
    '3rdparty/python:environ-config',
    'src/index:index-client',
    'src/lib/model',
  ],
  name='api-lib',
)   


pex_binary(
  name='api',
  dependencies=[
    ':api-lib',
    ':api-config',
  ],
  entry_point='app.py',
  inherit_path='fallback', # needed for connexion to be able to import pkg_resources
  zip_safe=False,
)