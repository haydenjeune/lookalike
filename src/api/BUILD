resources(
  name='api-config',
  sources=['spec.yaml'],
)

python_library(
  dependencies=[
    '3rdparty/python:connexion',
    '3rdparty/python:pillow',
    '3rdparty/python:environ-config',
    'src/index',
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
  zip_safe=False,
)