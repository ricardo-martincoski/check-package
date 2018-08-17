import pytest
import check_package as m


def test_import():
    assert m is not None


filename_to_lib = [
    (True, "package/tmux/tmux.mk", m.checkpackagelib.lib_mk),
    (True, "package/tmux/tmux.hash", m.checkpackagelib.lib_hash),
    (True, "package/tmux/0001-do-somthing.patch", m.checkpackagelib.lib_patch),
    (True, "package/tmux/Config.in", m.checkpackagelib.lib_config),
    (True, "package/tmux/Config.in.host", m.checkpackagelib.lib_config),
    (True, "package/tmux/Config.anything", m.checkpackagelib.lib_config),
    (False, "package/tmux/Config.in.host", m.checkpackagelib.lib_config),
    (True, "fs/common.mk", None),
    (False, "fs/common.mk", m.checkpackagelib.lib_mk),
    (True, "board/chromebook/snow/linux-4.15-dts-tpm.patch", None),
    (False, "board/chromebook/snow/linux-4.15-dts-tpm.patch", m.checkpackagelib.lib_patch),
    ]


@pytest.mark.parametrize("intree,filename,expected", filename_to_lib)
def test_filename_to_lib(intree, filename, expected):
    class flags():
        intree_only = intree
    m.flags = flags
    lib = m.get_lib_from_filename(filename)
    assert lib == expected
