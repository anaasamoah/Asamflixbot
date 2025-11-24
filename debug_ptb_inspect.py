import inspect
from telegram.ext import ApplicationBuilder
print('Signature:', inspect.signature(ApplicationBuilder.build))
import telegram.ext._jobqueue as jq
print('JobQueue present:', hasattr(jq, 'JobQueue'))
print('\nset_application source:')
print('\n'.join(inspect.getsource(jq.JobQueue.set_application).splitlines()[:200]))
