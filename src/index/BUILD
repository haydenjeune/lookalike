python_library(
  dependencies=[
    '3rdparty/python:environ-config',
    '3rdparty/python:grpcio',
    '3rdparty/python:protobuf',
    '3rdparty/python:faiss-cpu',
    'src/lib/index',
  ],
  name='index-lib',
)  

python_library(
  dependencies=[
    '3rdparty/python:grpcio',
    '3rdparty/python:protobuf',
  ],
  sources=['client.py'],
  name='index-client',
)  

pex_binary(
  name='index',
  dependencies=[
    ':index-lib',
  ],
  entry_point='main.py',
  zip_safe=False,
)