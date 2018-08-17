import pytest
import util
import checkpackagelib.lib_patch as m


apply_order = [
    ('path/0001-description.patch', '', []),
    ('path/1-description.patch', '', []),
    ('path/package-0001-description.patch', '', [
     ['path/package-0001-description.patch:0: use name <number>-<description>.patch (url#_providing_patches)']]),
    ('path/description.patch', '', [['path/description.patch:0: use name <number>-<description>.patch (url#_providing_patches)']]),
    ]


@pytest.mark.parametrize("filename,string,expected", apply_order)
def test_apply_order(filename, string, expected):
    warnings = util.check_file(m.ApplyOrder, filename, string)
    assert warnings == expected
