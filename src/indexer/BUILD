python_library(
  dependencies=[
    '3rdparty/python:environ-config',
    '3rdparty/python:faiss-cpu',
    'src/lib/index',
  ],
  name='indexer-lib',
)   


pex_binary(
  name='indexer',
  dependencies=[
    ':indexer-lib',
  ],
  entry_point='main.py',
  zip_safe=False,
)