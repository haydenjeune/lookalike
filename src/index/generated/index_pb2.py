# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: index.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='index.proto',
  package='index',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0bindex.proto\x12\x05index\"2\n\x0bIndexSearch\x12\x0e\n\x06vector\x18\x01 \x01(\x0c\x12\x13\n\x0bnum_results\x18\x02 \x01(\r\"5\n\x0cIndexResults\x12%\n\x0b\x63\x65lebrities\x18\x01 \x03(\x0b\x32\x10.index.Celebrity\"-\n\tCelebrity\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x12\n\nsimilarity\x18\x02 \x01(\x02\x32<\n\x05Index\x12\x33\n\x06Search\x12\x12.index.IndexSearch\x1a\x13.index.IndexResults\"\x00\x62\x06proto3'
)




_INDEXSEARCH = _descriptor.Descriptor(
  name='IndexSearch',
  full_name='index.IndexSearch',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='vector', full_name='index.IndexSearch.vector', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='num_results', full_name='index.IndexSearch.num_results', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=22,
  serialized_end=72,
)


_INDEXRESULTS = _descriptor.Descriptor(
  name='IndexResults',
  full_name='index.IndexResults',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='celebrities', full_name='index.IndexResults.celebrities', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=74,
  serialized_end=127,
)


_CELEBRITY = _descriptor.Descriptor(
  name='Celebrity',
  full_name='index.Celebrity',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='index.Celebrity.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='similarity', full_name='index.Celebrity.similarity', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=129,
  serialized_end=174,
)

_INDEXRESULTS.fields_by_name['celebrities'].message_type = _CELEBRITY
DESCRIPTOR.message_types_by_name['IndexSearch'] = _INDEXSEARCH
DESCRIPTOR.message_types_by_name['IndexResults'] = _INDEXRESULTS
DESCRIPTOR.message_types_by_name['Celebrity'] = _CELEBRITY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

IndexSearch = _reflection.GeneratedProtocolMessageType('IndexSearch', (_message.Message,), {
  'DESCRIPTOR' : _INDEXSEARCH,
  '__module__' : 'index_pb2'
  # @@protoc_insertion_point(class_scope:index.IndexSearch)
  })
_sym_db.RegisterMessage(IndexSearch)

IndexResults = _reflection.GeneratedProtocolMessageType('IndexResults', (_message.Message,), {
  'DESCRIPTOR' : _INDEXRESULTS,
  '__module__' : 'index_pb2'
  # @@protoc_insertion_point(class_scope:index.IndexResults)
  })
_sym_db.RegisterMessage(IndexResults)

Celebrity = _reflection.GeneratedProtocolMessageType('Celebrity', (_message.Message,), {
  'DESCRIPTOR' : _CELEBRITY,
  '__module__' : 'index_pb2'
  # @@protoc_insertion_point(class_scope:index.Celebrity)
  })
_sym_db.RegisterMessage(Celebrity)



_INDEX = _descriptor.ServiceDescriptor(
  name='Index',
  full_name='index.Index',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=176,
  serialized_end=236,
  methods=[
  _descriptor.MethodDescriptor(
    name='Search',
    full_name='index.Index.Search',
    index=0,
    containing_service=None,
    input_type=_INDEXSEARCH,
    output_type=_INDEXRESULTS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_INDEX)

DESCRIPTOR.services_by_name['Index'] = _INDEX

# @@protoc_insertion_point(module_scope)
