#!/usr/bin/env python

from __future__ import division, print_function
import os
import sys
import ast
try:
    import numpy
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from . import inputText
from . import builtins
from .symboltable import SymbolTable, Group, isgroup
from .util import LarchExceptionHolder, Procedure, DefinedVariable
from .closure import Closure

__version__ = '0.9.3'

def iscallable(obj):
    return hasattr(obj, '__call__')

if sys.version_info[0] == 2:
    def iscallable(obj):
        return callable(obj) or hasattr(obj, '__call__')
        
class Interpreter:
    """larch program compiler and interpreter.
  This module compiles expressions and statements to AST representation,
  using python's ast module, and then executes the AST representation
  using a custom SymbolTable for named object (variable, functions).
  This then gives a restricted version of Python, with slightly modified
  namespace rules.  The program syntax here is expected to be valid Python,
  but that may have been translated as with the inputText module.

  The following Python syntax is not supported:
      Exec, Lambda, Class, Global, Generators, Yield, Decorators
        
  In addition, Function is greatly altered so as to allow a Larch procedure.
  """

    supported_nodes = ('assert', 'assign', 'attribute', 'augassign', 'binop',
                       'boolop', 'break', 'call', 'compare', 'continue',
                       'delete', 'dict', 'ellipsis', 'excepthandler', 'expr',
                       'expression', 'extslice', 'for', 'functiondef', 'if',
                       'ifexp', 'import', 'importfrom', 'index', 'interrupt',
                       'list', 'listcomp', 'module', 'name', 'num', 'pass',
                       'print', 'raise', 'repr', 'return', 'slice', 'str',
                       'subscript', 'tryexcept', 'tuple', 'unaryop', 'while')

    def __init__(self, symtable=None, writer=None):
        self.writer = writer or sys.stdout
       
        if symtable is None:
            symtable = SymbolTable(larch=self)
        self.symtable   = symtable
        self._interrupt = None
        self.error      = [] 
        self.expr       = None
        self.retval     = None
        self.fname     = '<StdInput>'
        self.lineno    = -5
        builtingroup = getattr(symtable,'_builtin')
        mathgroup    = getattr(symtable,'_math')

        for sym in builtins.from_builtin:
            setattr(builtingroup, sym, __builtins__[sym])

        if HAS_NUMPY:
            for sym in builtins.from_numpy:
                setattr(mathgroup, sym, getattr(numpy, sym))
            
                for fname, sym in list(builtins.numpy_renames.items()):
                    setattr(mathgroup, fname, getattr(numpy, sym))

        for fname, fcn in list(builtins.local_funcs.items()):
            setattr(builtingroup, fname,
                    Closure(func=fcn, larch=self))
        setattr(builtingroup, 'definevar',
                Closure(func=self.set_definedvariable))
        
    def set_definedvariable(self, name, expr):
        """define a defined variable (re-evaluate on access)"""
        self.symtable.set_symbol(name,
                                 DefinedVariable(expr=expr, larch=self))

    def unimplemented(self, node):
        "unimplemented nodes"
        self.raise_exception(node,
                             "'%s' not supported" % (node.__class__.__name__),
                             py_exc=sys.exc_info())

    def raise_exception(self, node, msg='', expr=None,
                        fname=None, lineno=-1, py_exc=None):
        "add an exception"
        if self.error is None:
            self.error = []
        if expr  is None:
            expr  = self.expr
        if fname is None:
            fname = self.fname        
        if lineno is None:
            lineno = self.lineno

        if len(self.error) > 0 and not isinstance(node, ast.Module):
            msg = 'Extra Error (%s)' % msg

        if py_exc is None:
            etype, evalue = None, None
        else:
            etype, evalue, tback = py_exc
        # print( "RAISE ", msg, tback)
        err = LarchExceptionHolder(node, msg=msg, expr= expr,
                                   fname= fname, lineno=lineno,
                                   py_exc=(etype, evalue) )
        self._interrupt = ast.Break()
        self.error.append(err)
        self.symtable._sys.last_error = err

        # print("_Raise ", self.error)
        
    # main entry point for Ast node evaluation
    #  compile:  string statement -> ast
    #  interp :  ast -> result
    #  eval   :  string statement -> result = interp(compile(statement))
    def compile(self, text, fname=None, lineno=-4):
        """compile statement/expression to Ast representation    """
        self.expr  = text
        try:
            return ast.parse(text)
        except:
            self.raise_exception(None, msg='Syntax Error',
                                 expr=text, fname=fname, lineno=lineno,
                                 py_exc=sys.exc_info())
            
    def interp(self, node, expr=None, fname=None, lineno=None):
        """executes compiled Ast representation for an expression"""
        # Note: keep the 'node is None' test: internal code here may run
        #    interp(None) and expect a None in return.
        if node is None:
            return None
        if isinstance(node, str):
            node = self.compile(node)
        if lineno is not None:
            self.lineno = lineno
        if fname  is not None:
            self.fname  = fname
        if expr   is not None:
            self.expr   = expr
       
        # get handler for this node:
        #   on_xxx with handle nodes of type 'xxx', etc
        try:
            handler = self.node_handlers[node.__class__.__name__.lower()]
        except KeyError:
            return self.unimplemented(node)

        # run the handler:  this will likely generate
        # recursive calls into this interp method.
        try:
            #print(" Interp NODE ", ast.dump(node))
            ret = handler(node)
            if isinstance(ret, enumerate):
                ret = list(ret)
            return ret

        except:
            self.raise_exception(node, msg='Runtime Error',
                                 expr=expr, fname=fname, lineno=lineno,
                                 py_exc=sys.exc_info())              
            
    def __call__(self, expr, **kw):
        return self.eval(expr, **kw)
        
    def eval(self, expr, fname=None, lineno=0):
        """evaluates a single statement"""
        self.fname = fname        
        self.lineno = lineno
        self.error = []

        node = self.compile(expr, fname=fname, lineno=lineno)
        # print("COMPILE ", ast.dump(node))
        out = None
        if len(self.error) > 0:
            self.raise_exception(node, msg='Eval Error', expr=expr,
                                 fname=fname, lineno=lineno,
                                 py_exc=sys.exc_info())
        else:            
            # print(" -> interp ", node, expr,  fname, lineno)
            out = self.interp(node, expr=expr,
                              fname=fname, lineno=lineno)

        if len(self.error) > 0:
            self.raise_exception(node, msg='Eval Error', expr=expr,
                                 fname=fname, lineno=lineno,
                                 py_exc=sys.exc_info())
        return out
        
    def dump(self, node, **kw):
        "simple ast dumper"
        return ast.dump(node, **kw)

class LarchToPython(ast.NodeTransformer):
    def visit_Name(self, node):
        '''Name node'''

        dispatch = dict(ast.Del="self.symtable.del_symbol

        ctx = node.ctx.__class__
        if ctx
