import ctypes
import os
from os.path import dirname, join, exists
from shutil import which
from libghdl.config import __version__


def _get_libghdl_name():
    """Get the name of the libghdl library (with version and extension)"""
    ver = __version__.replace('-', '_').replace('.', '_')
    ext = {'win32': 'dll',
           'cygwin': 'dll',
           'darwin': 'dylib'}.get(os.name, 'so')
    return 'libghdl-' + ver + '.' + ext


def _check_libghdl_libdir(libdir, basename):
    """Return libghdl path in :param libdir" if found or None"""
    if libdir is None:
        return None
    # print('libghdl: check in {}'.format(libdir))
    res = join(libdir, basename)
    if exists(res):
        return res
    return None


def _check_libghdl_bindir(bindir, basename):
    if bindir is None:
        return None
    return _check_libghdl_libdir(join(bindir, '..', 'lib'), basename)


def _get_libghdl_path():
    """Locate the directory where the shared library is"""
    basename = get_libghdl_name()
    # Try VUNIT_GHDL_PATH (path of the ghdl binary when using VUnit).
    r = _check_libghdl_bindir (os.environ.get('VUNIT_GHDL_PATH'), basename)
    if r is not None:
        return r
    # Try GHDL (name/path of the ghdl binary)
    r = os.environ.get('GHDL', 'ghdl')
    r = which(r)
    if r is not None:
        r = _check_libghdl_bindir(dirname(r), basename)
        if r is not None:
            return r
    # Try within libghdl/ python installation
    r = __file__
    r = _check_libghdl_bindir(dirname(r), basename)
    if r is not None:
        return r
    # Try when running from the build directory
    r = join(dirname(__file__), '..', '..', 'lib')
    r = _check_libghdl_libdir(r, basename)
    if r is not None:
        return r
    # Failed.
    raise Exception('Cannot find libghdl {}'.format(basename))


# Load the shared library
_libghdl_path = _get_libghdl_path()
libghdl = ctypes.CDLL(_libghdl_path)

# Initialize it.
libghdl.libghdl_init()


def _to_char_p(arg):
    return ctypes.c_char_p(arg), len(arg)


def set_option(opt):
    return libghdl.libghdl__set_option(*_to_char_p(opt))


def analyze_init():
    return libghdl.libghdl__analyze_init()


def analyze_file(fname):
    return libghdl.libghdl__analyze_file(*_to_char_p(fname))


if False:
    _prefix = os.environ.get("LIBGHDL_PREFIX") or '--PREFIX=%s' % join(dirname(_libghdl_path), 'ghdl')
    # print('ghdl prefix: {}'.format(_prefix))
    set_option(_prefix.encode('utf-8'))