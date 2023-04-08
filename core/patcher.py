import json, shutil, os

from core.constants import *

from core.extractor import StringLiteralExtractor
from core.models.stringliteral import StringLiteral

class StringLiteralPatcher:
  def __init__(self, metadata_filepath, stringliteral_filepath):
    self.metadata_filepath = metadata_filepath
    self.stringliteral_filepath = stringliteral_filepath
    self.patched_stringliterals = []

    self.extractor = StringLiteralExtractor(metadata_filepath)
    self.extractor.extract()

  def update(self):
    with open(self.stringliteral_filepath, 'r') as f:
      self._populate_patched_stringliterals(f)
    self._update_extractor_data()
    return self

  def patch(self, output_filepath):
    shutil.copy2(self.metadata_filepath, output_filepath)

    with open(output_filepath, 'rb+') as f:
      self._patch(f)

  def _populate_patched_stringliterals(self, f):
    data = json.load(f)
    self.patched_stringliterals = [StringLiteral.from_dict(entry) for entry in data]

  def _update_extractor_data(self):
    for entry in self.patched_stringliterals:
      value_bytes = bytes(entry.value, 'utf-8')
      new_length = len(value_bytes)
      index = entry.index
      self.extractor.lookup_table[index].length = new_length
      self.extractor.stringliterals[index].value = entry.value

    index = 0
    for entry in self.extractor.lookup_table:
      entry.index = index
      index += entry.length

  def _patch(self, f):
    offset = self._get_last_offset(f)
    self._append_stringliteral_database(f, offset)
    self._patch_lookup_table(f)
    self._patch_stringliteral_data_offset(f, offset)

  def _get_last_offset(self, f):
    f.seek(0, os.SEEK_END)
    offset = f.tell()
    f.seek(0)

    return offset

  def _append_stringliteral_database(self, f, offset):
    f.seek(offset)
    for entry in self.extractor.stringliterals:
      f.write(bytes(entry.value, 'utf-8'))
    f.seek(0)

  def _patch_lookup_table(self, f):
    lookup_table_offset = self._get_lookup_table_offset(f)
    f.seek(lookup_table_offset)

    for entry in self.extractor.lookup_table:
      f.write(entry.length.to_bytes(4, byteorder='little'))
      f.write(entry.index.to_bytes(4, byteorder='little'))

  def _patch_stringliteral_data_offset(self, f, offset):
    f.seek(STRINGLITERAL_DATA_DEFINITION_OFFSET)
    f.write(offset.to_bytes(4, byteorder='little'))

  def _get_lookup_table_offset(self, f):
    f.seek(LOOKUP_TABLE_DEFINITION_OFFSET)
    return int.from_bytes(f.read(4), byteorder='little')
