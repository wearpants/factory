import new

def importString(source, filename, globals_=None, locals_=None):
    """construct a module from source code.
    
    The module will I{not} appear in L{sys.modules}.
    
    @arg source: source code of the module
    @type source: string
    
    @arg filename: a filename to use for the module's __file__
    @type filename: string
    
    @arg globals_: globals to pass to L{eval}(). Defaults to globals()
    @type globals_: dict

    @arg locals_: locals to pass to L{eval}(). Defaults to empty dict
    @type locals_: dict    
    
    @rtype: a module
    """
    if globals_ is None: globals_ = globals()
    if locals_ is None: locals_ = {}
    locals_['__file__'] = filename
    co = compile(source, filename, 'exec')
    eval(co, globals_, locals_)
    mod = new.module(os.path.splitext(os.path.basename(filename))[0])
    mod.__dict__.update(locals_)
    return mod

def importFile(f, filename=None, globals_=None, locals_=None):
    """construct a module from a file
    
    The module will I{not} appear in L{sys.modules}.  The key difference between this function and __import__ is that the file need not be present in L{sys.path}.
    
    @arg f: filename or open file
    @type f: string or L{file}
    
    @arg globals_: globals to pass to L{eval}(). Defaults to globals()
    @type globals_: dict

    @arg locals_: locals to pass to L{eval}(). Defaults to empty dict
    @type locals_: dict    
    
    @rtype: a module
    """
    if isinstance(f, str):
        f = file(f, 'r')
    if filename is None:
        filename = f.name
    return importString(f.read(), filename, globals_, locals_)