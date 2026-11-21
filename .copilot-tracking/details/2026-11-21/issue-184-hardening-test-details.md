# Details

Edit only infra/tests/test_container_hosting_144.py. Add helper `_resolve_param_default(template, value)`: if value matches `[parameters('<name>')]`, return template["parameters"][name]["defaultValue"], else value.
