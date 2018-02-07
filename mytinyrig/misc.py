import os
import imp


def try_import(path, module_name):
    try:
        mod = imp.load_module(module_name, None,
                              os.path.join(path, module_name),
                              ('', '', 5))
    except ImportError:
        init_path = os.path.join(path, module_name, '__init__.py')
        try:
            with open(init_path, 'a'):
                os.utime(init_path, None)
            mod = imp.load_module(module_name, None,
                                  os.pathh.join(path, module_name),
                                  ('', '', 5))
        except IOError:
            raise Exception(('There is no directory in the path %s. '
                             'Check your configuration or create '
                             'the directory in the desired path.') %
                            os.path.join(path, module_name))
    return mod


def package_files(package, extension):
    pathname = package.__path__[0]
    return set([os.path.abspath(os.path.join(pathname, file))
                for file in os.listdir(pathname)
                if file.endswith(extension)])
