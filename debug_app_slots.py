import inspect
import telegram.ext._application as appmod
Application = appmod.Application
print('Application repr:', Application)
print('__slots__' in Application.__dict__)
print('slots:', Application.__dict__.get('__slots__'))
print('is instance of type?', isinstance(Application, type))
print('bases:', Application.__bases__)
print('has __weakref__ attribute in dict?', '__weakref__' in Application.__dict__)
print('mro:', Application.__mro__)

# Try to instantiate without building (may require args), so just inspect dataclass or attrs
try:
    src = inspect.getsource(Application)
    for i,l in enumerate(src.splitlines()[:200],1):
        print(f"{i:03}: {l}")
except Exception as e:
    print('Could not get source of Application:', e)
