import json

from core.constants import *

from core.models.stringliteral import StringLiteral
from core.models.lookup_table_entry import LookupTableEntry


class StringLiteralExtractor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lookup_table = []
        self.stringliterals = []

        self.last_byte = 0

    def extract(self):
        with open(self.filepath, "rb") as f:
            self._extract(f)
        return self

    def dump(self, output_path):
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.to_dict(), indent=2, ensure_ascii=False))

    def _extract(self, f):
        self._ensure_magic_is_valid(f)

        lookup_table_offset = self._get_lookup_table_offset(f)
        lookup_table_size = self._get_lookup_table_size(f)
        stringliteral_data_offset = self._get_stringliteral_data_offset(f)
        stringliteral_data_size = self._get_stringliteral_data_size(f)

        self._extract_lookup_table(f, lookup_table_offset, lookup_table_size)
        self._extract_string_literals(
            f, stringliteral_data_offset, stringliteral_data_size
        )

    def _ensure_magic_is_valid(self, f):
        magic = f.read(4)
        if magic != MAGIC_BYTES:
            raise Exception("Invalid global-metadata file")

    def _get_lookup_table_offset(self, f):
        f.seek(LOOKUP_TABLE_DEFINITION_OFFSET)
        return int.from_bytes(f.read(4), byteorder="little")

    def _get_lookup_table_size(self, f):
        f.seek(LOOKUP_TABLE_SIZE_DEFINITION_OFFSET)
        return int.from_bytes(f.read(4), byteorder="little")

    def _get_stringliteral_data_offset(self, f):
        f.seek(STRINGLITERAL_DATA_DEFINITION_OFFSET)
        return int.from_bytes(f.read(4), byteorder="little")

    def _get_stringliteral_data_size(self, f):
        f.seek(STRINGLITERAL_DATA_SIZE_DEFINITION_OFFSET)
        return int.from_bytes(f.read(4), byteorder="little")

    def _extract_lookup_table(self, f, lookup_table_offset, lookup_table_size):
        f.seek(lookup_table_offset)

        bytes_read = 0
        while bytes_read < lookup_table_size:
            length = int.from_bytes(f.read(4), byteorder="little")
            index = int.from_bytes(f.read(4), byteorder="little")
            self._add_lookup_table_entry(length, index)
            bytes_read += 8

    def _extract_string_literals(
        self, f, stringliteral_data_offset, stringliteral_data_size
    ):
        f.seek(stringliteral_data_offset)

        for idx, entry in enumerate(self.lookup_table):
            f.seek(stringliteral_data_offset + entry.index)
            literal = f.read(entry.length).decode("utf-8", "ignore")
            self._add_string_literal(idx, literal)

    def _add_lookup_table_entry(self, length, index):
        lookup_table_entry = LookupTableEntry(length, index)
        self.lookup_table.append(lookup_table_entry)

    def _add_string_literal(self, index, literal):
        string_literal = StringLiteral(index, literal)
        self.stringliterals.append(string_literal)

    def to_dict(self):
        return [string_literal.to_dict() for string_literal in self.stringliterals]
