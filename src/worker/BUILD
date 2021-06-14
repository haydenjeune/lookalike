python_library(
  dependencies=[
    '3rdparty/python:environ-config',
    'src/lib/index',
  ],
  name='worker-lib',
)   


pex_binary(
  name='worker',
  dependencies=[
    ':worker-lib',
  ],
  entry_point='main.py',
  zip_safe=False,
)