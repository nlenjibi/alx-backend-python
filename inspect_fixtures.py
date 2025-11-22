import importlib.util
import os
from pprint import pprint
path = os.path.join('0x03-Unittests_and_integration_tests', 'test_client.py')
import sys
sys.path.insert(0, os.path.dirname(path))
spec = importlib.util.spec_from_file_location('test_client', path)
module = importlib.util.module_from_spec(spec)
import sys as _sys
_sys.modules['test_client'] = module
spec.loader.exec_module(module)
for name in dir(module):
    if name.startswith('TestIntegrationGithubOrgClient'):
        cls = getattr(module, name)
        print('CLASS', name)
        for attr in ('org_payload','repos_payload','expected_repos','apache2_repos'):
            val = getattr(cls, attr, None)
            print(attr, type(val), repr(val)[:200])
