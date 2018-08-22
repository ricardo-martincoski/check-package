import pytest
import util
import checkpackagelib.lib_hash as m


hash_number_of_fields = [
    ('any', '', []),
    ('any', '\n', []),
    ('any', '\t\n', []),
    ('any', '# text\n', []),
    ('any', 'field1\n', [['any:1: expected three fields (url#adding-packages-hash)', 'field1\n']]),
    ('any', 'field1 field2\n', [['any:1: expected three fields (url#adding-packages-hash)', 'field1 field2\n']]),
    ('any', 'field1 field2 field3 field4\n', [
     ['any:1: expected three fields (url#adding-packages-hash)', 'field1 field2 field3 field4\n']]),
    ('any', 'field1 field2 field3\n', []),
    ('any', '   field1   field2   field3\n', []),
    ('any', 'field1\tfield2\tfield3\n', []),
    ('any', '\tfield1\t field2\t field3 \n', []),
    ]


@pytest.mark.parametrize("filename,string,expected", hash_number_of_fields)
def test_hash_number_of_fields(filename, string, expected):
    warnings = util.check_file(m.HashNumberOfFields, filename, string)
    assert warnings == expected


hash_type = [
    ('any', '', []),
    ('any', 'text\n', []),
    ('any', 'text text\n', [['any:1: unexpected type of hash (url#adding-packages-hash)', 'text text\n']]),
    ('any', 'none text\n', []),
    ('any', 'md5 123456\n', [
     ['any:1: hash size does not match type (url#adding-packages-hash)', 'md5 123456\n', 'expected 32 hex digits']]),
    ('any', 'md5 12345678901234567890123456789012\n', []),
    ('any', ' md5 12345678901234567890123456789012\n', []),
    ('any', 'md5  12345678901234567890123456789012\n', []),
    ('any', 'md5\t12345678901234567890123456789012\n', []),
    ('any', 'md5sum 12345678901234567890123456789012\n', [
     ['any:1: unexpected type of hash (url#adding-packages-hash)', 'md5sum 12345678901234567890123456789012\n']]),
    ('any', 'md5 123456789012345678901234567890123\n', [
     ['any:1: hash size does not match type (url#adding-packages-hash)',
      'md5 123456789012345678901234567890123\n',
      'expected 32 hex digits']]),
    ('any', 'sha1 1234567890123456789012345678901234567890\n', []),
    ('any', 'sha256 1234567890123456789012345678901234567890123456789012345678901234\n', []),
    ('any', 'sha384 123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456\n', []),
    ('any', 'sha512 1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
     '1234567890123456789012345678\n', []),
    ]


@pytest.mark.parametrize("filename,string,expected", hash_type)
def test_hash_type(filename, string, expected):
    warnings = util.check_file(m.HashType, filename, string)
    assert warnings == expected
