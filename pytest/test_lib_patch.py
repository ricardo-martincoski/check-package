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


numbered_subject = [
    ('patch', '', []),
    ('patch', 'Subject: [PATCH 24/105] text\n', []),
    ('patch', 'Subject: [PATCH 24/105] text\ndiff --git a/configure.ac b/configure.ac\n', [
     ["patch:1: generate your patches with 'git format-patch -N'", 'Subject: [PATCH 24/105] text\n']]),
    ('patch', 'Subject: [PATCH] text\ndiff --git a/configure.ac b/configure.ac\n', []),
    ]


@pytest.mark.parametrize("filename,string,expected", numbered_subject)
def test_numbered_subject(filename, string, expected):
    warnings = util.check_file(m.NumberedSubject, filename, string)
    assert warnings == expected


sob = [
    ('patch', 'Signed-off-by: John Doe <johndoe@example.com>\n', []),
    ('patch', '', [
     ['patch:0: missing Signed-off-by in the header (url#_format_and_licensing_of_the_package_patches)']]),
    ('patch', 'Subject: [PATCH 24/105] text\n', [
     ['patch:0: missing Signed-off-by in the header (url#_format_and_licensing_of_the_package_patches)']]),
    ]


@pytest.mark.parametrize("filename,string,expected", sob)
def test_sob(filename, string, expected):
    warnings = util.check_file(m.Sob, filename, string)
    assert warnings == expected
