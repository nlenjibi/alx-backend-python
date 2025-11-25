import importlib.util, sys, os
path = os.path.abspath('0x03-Unittests_and_integration_tests')
sys.path.insert(0, path)
spec = importlib.util.spec_from_file_location('tc', os.path.join(path, 'test_client.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
classes = [(n, c) for n, c in m.__dict__.items() if n.startswith('TestIntegrationGithubOrgClient') and isinstance(c, type)]
print('Found classes:', [n for n, _ in classes])
for n, c in classes:
    print('CLASS:', n)
    print('  org_payload type:', type(getattr(c, 'org_payload', None)))
    print('  org_payload repr:', repr(getattr(c, 'org_payload', None))[:200])
    print('  repos_payload type:', type(getattr(c, 'repos_payload', None)))
    print('  repos_payload repr:', repr(getattr(c, 'repos_payload', None))[:200])
    print('  expected_repos type:', type(getattr(c, 'expected_repos', None)))
    print('  apache2_repos type:', type(getattr(c, 'apache2_repos', None)))
