#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import copy
from glob import glob
from itertools import chain
from pydoc import pager
import help

from .symboltable import Group, GroupAlias

helper = help.Helper()

# inherit these from python's __builtins__
from_builtin= ('ArithmeticError', 'AssertionError', 'AttributeError',
                'BaseException', 'BufferError', 'BytesWarning',
                'DeprecationWarning', 'EOFError', 'EnvironmentError',
                'Exception', 'False', 'FloatingPointError',
                'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning',
                'IndentationError', 'IndexError', 'KeyError',
                'KeyboardInterrupt', 'LookupError', 'MemoryError',
                'NameError', 'None', 'NotImplemented',
                'NotImplementedError', 'OSError', 'OverflowError',
                'ReferenceError', 'RuntimeError', 'RuntimeWarning',
                'StandardError', 'StopIteration', 'SyntaxError',
                'SyntaxWarning', 'SystemError', 'SystemExit', 'True',
                'TypeError', 'UnboundLocalError', 'UnicodeDecodeError',
                'UnicodeEncodeError', 'UnicodeError',
                'UnicodeTranslateError', 'UnicodeWarning', 'ValueError',
                'Warning', 'ZeroDivisionError', 'abs', 'all', 'any',
                'apply', 'basestring', 'bin', 'bool', 'buffer',
                'bytearray', 'bytes', 'callable', 'chr', 'cmp', 'coerce',
                'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate',
                'file', 'filter', 'float', 'format', 'frozenset',
                'getattr', 'hasattr', 'hash', 'hex', 'id', 'int',
                'isinstance', 'len', 'list', 'map', 'max', 'min', 
                'oct', 'open', 'ord', 'pow', 'property', 'range',
                'raw_input', 'reduce', 'repr', 'reversed', 'round', 'set',
                'setattr', 'slice', 'sorted', 'str', 'sum', 'tuple',
                'type', 'unichr', 'unicode', 'zip')

# inherit these from numpy

from_numpy = ('pi','e', 'array','sin','cos','tan','exp','log','log10',
               'sqrt','arange', 'arccos', 'arccosh', 'arcsin', 'arcsinh',
               'arctan', 'arctan2', 'arctanh', 'argmax', 'argmin',
               'argsort', 'array', 'cosh', 'fabs', 'floor', 'floor_divide',
               'fmod', 'tanh', 'sign', 'sinh', 'identity', 'take',
               'choose', 'add', 'allclose', 'alltrue', 'around', 'asarray',
               'average', 'bitwise_and', 'bitwise_or', 'bitwise_xor',
               'ceil', 'clip', 'compress', 'concatenate', 'conjugate',
               'convolve', 'cumproduct', 'cumsum', 'diagonal', 'divide',
               'dot', 'equal', 'greater', 'greater_equal', 'hypot',
               'indices', 'invert', 'left_shift', 'less', 'less_equal',
               'logical_and', 'logical_not', 'logical_or', 'logical_xor',
               'maximum', 'minimum', 'multiply', 'negative', 'nonzero',
               'not_equal', 'ones', 'outer', 'power', 'product', 'put',
               'putmask', 'rank', 'ravel', 'remainder', 'repeat',
               'reshape', 'resize', 'right_shift', 'searchsorted', 'shape',
               'size', 'sometrue', 'sort', 'subtract', 'sum', 'swapaxes',
               'trace', 'transpose', 'true_divide', 'vdot', 'where',
               'zeros','linspace')

numpy_renames ={'ln':'log',
                 'atan':'arctan',
                 'atan2':'arctan2',
                 'acos':'arccos',
                 'acosh':'arccosh',
                 'asin':'arcsin',
                 'asinh':'arcsinh'}
                 
##
## More builtin commands, to set up the larch language:
## Closures will be used to make sure these are always called with a valid
## larch interpreter as the larch parameter.
##
def _group(larch=None,**kw):
    """create a group"""
    # try:
    g = larch.symtable.create_group()
    for k,v in kw.items():
        setattr(g,k,v)
    return g
#     except:
#         return None

def _showgroup(gname=None,larch=None):
    if larch is None:
        raise Warning("cannot show group -- larch broken?")

    if gname is None:
        gname = '_main'
    return larch.symtable.show_group(gname)

def _copy(obj,**kw): # pragma: no cover
    return copy.deepcopy(obj)

def _run(name, larch=None, **kw):
    "run a larch file"
    if larch is None:
        raise Warning("cannot run file '%s' -- larch broken?" % name)

    larch.eval_file(name)

def _which(name, larch=None, **kw):
    "print out fully resolved name of a symbol"
    if larch is None:
        raise Warning("cannot locate symobol '%s' -- larch broken?" % name)

    print("Find symbol %s" % name, file=larch.writer)
    print(larch.symtable.get_parent(name), file=larch.writer)
    

def _reload(mod,larch=None,**kw):
    """reload a module, either larch or python"""

    if larch is None: return None

    if isinstance(mod, str):
        return larch.import_module(mod, do_reload=True)

    for k,v in chain(larch.symtable._sys.modules.iteritems(), sys.modules.iteritems()):
        if v == mod:
            modname = k
            break
    try:
        return larch.import_module(modname,do_reload=True)
    except NameError:
        pass

def show_more(text,filename=None,writer=None,pagelength=30,prefix=''):
    """show lines of text in the style of more """

    pager(text)

def _ls(dir='.', **kws):
    " return list of files in the current directory "
    dir.strip()
    if len(dir) == 0: arg = '.'
    if os.path.isdir(dir):
        ret = os.listdir(dir)
    else:
        ret = glob(dir)
    if sys.platform == 'win32':
        for i, r in enumerate(ret):
            ret[i] = ret[i].replace('\\','/')
    return ret


def _cwd(x=None, **kws):
    "return current working directory"
    ret = os.getcwd()
    if sys.platform == 'win32':
        ret = ret.replace('\\','/')
    return ret

def _cd(name,**kwds):
    "change directorty"
    name = name.strip()
    if name:
        os.chdir(name)

    ret = os.getcwd()
    if sys.platform == 'win32':
        ret = ret.replace('\\','/')
    return ret

def _more(name,pagelength=24,larch=None, **kws):
    "list file contents"
    try:
        with open(name) as inf:
            show_more(inf.read())
    except IOError:
        print("cannot open file: %s." % name, file=larch.writer)
    
def _help(*args,**kws):
    "show help on topic or object"
    helper.buffer = []
    larch = kws.get('larch',None)
    if helper.larch is None and larch is not None:  helper.larch = larch
    if args == ('',):
        args = ('help',)
    if helper.larch is None:
        helper.addtext('cannot start help system!')
    else:
        [helper.help(a.strip()) for a in args]

    return helper.getbuffer()

def _cs(namespace, larch=None, **kws):
    '''change the symbol table to alter how names are resolved.

    This is a convenience function for interactive use which lets the user
    specify the namespace (larch Group) in which to look first. If namespace is
    not already a Group, then a GroupAlias is made for it.

    Args:
        namespace
    '''

    if larch is None: return
    if not isinstance(namespace, Group):
        namespace = GroupAlias(obj=namespace, name="Alias for %s" % namespace)
    larch.symtable._sys.localGroup = namespace
    
local_funcs = {'group':_group,
               'showgroup':_showgroup,
               'reload':_reload,
               'copy': _copy,
               'more': _more,
               'ls': _ls,
               'cd': _cd,
               'run': _run,
               'which': _which,                
               'cwd': _cwd, 
               'help': _help,
               'cs': _cs
               }
       
