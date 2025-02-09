from openapi_spec_validator import validate
from openapi_spec_validator.readers import read_from_filename

def test_validate_spec():
    spec_dict, base_uri = read_from_filename('openapi.yml')
    validate(spec_dict)