python_library(
  dependencies=[
    '3rdparty/python:environ-config',
    '3rdparty/python:beautifulsoup4',
  ],
  name='scraper-lib',
)

pex_binary(
  name='scraper',
  dependencies=[
    ':scraper-lib',
  ],
  entry_point='main.py',
  zip_safe=False,
)