import inspect
import telegram.ext._applicationbuilder as ab
src = inspect.getsource(ab)
for i,l in enumerate(src.splitlines(), start=1):
    if 'def build' in l or 'class Application' in l or 'Application(' in l:
        print(f"{i:04}: {l}")
# print the build function body
b = inspect.getsource(ab.ApplicationBuilder.build)
print('\n--- build func ---')
for i,l in enumerate(b.splitlines(),1):
    print(f"{i:03}: {l}")
