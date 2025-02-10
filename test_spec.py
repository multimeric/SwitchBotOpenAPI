from dataclasses import dataclass, field
from typing import Any, Mapping, Optional
from openapi_spec_validator import validate
from openapi_spec_validator.readers import read_from_filename
import pytest
from openapi_core import OpenAPI
from openapi_core.datatypes import RequestParameters
from openapi_python_client.schema import openapi_schema_pydantic as osp
from ruamel.yaml import YAML

@dataclass
class FakeRequest:
    path: str
    host_url: str = "https://api.switch-bot.com"
    parameters: RequestParameters = field(default_factory=lambda : RequestParameters())
    #: Note that this must be lowercase
    method: str = 'get'
    body: Optional[bytes] = None
    content_type: str = 'application/json'

@dataclass
class FakeReponse:
    status_code: int = 200
    content_type: str = "application/json"
    headers: Mapping[str, Any] = field(default_factory=dict)
    data: Optional[bytes] = None

@dataclass
class ReqResPair:
    request: FakeRequest
    response: FakeReponse

@pytest.fixture
def openapi() -> OpenAPI:
    return OpenAPI.from_file_path('openapi.yml')

def test_validate_openapi_spec_validator():
    """
    Test the validity of the spec itself using openapi_spec_validator
    """
    spec_dict, _base_uri = read_from_filename('openapi.yml')
    validate(spec_dict)

def test_validate_openapi_python_client():
    """
    Test the validity of the spec itself using openapi_python_client
    """
    yaml = YAML(typ='safe', pure=True)
    with open('openapi.yml') as f:
        osp.OpenAPI.model_validate(yaml.load(f))

@pytest.mark.parametrize('pair', [
    ReqResPair(
        request=FakeRequest(path='/v1.1/devices'),
        response=FakeReponse(data=b"""{
            "statusCode": 100,
            "body": {
                "deviceList": [
                    {
                        "deviceId": "500291B269BE",
                        "deviceName": "Living Room Humidifier",
                        "deviceType": "Humidifier",
                        "enableCloudService": true,
                        "hubDeviceId": "000000000000"
                    }
                ],
                "infraredRemoteList": [
                    {
                        "deviceId": "02-202008110034-13",
                        "deviceName": "Living Room TV",
                        "remoteType": "TV",
                        "hubDeviceId": "FA7310762361"
                    }
                ]
            },
            "message": "success"
        }""")
    ),
    ReqResPair(
        request=FakeRequest(path='/v1.1/devices/C271111EC0AB/status'),
        response=FakeReponse(data=b"""{
            "statusCode": 100,
            "body": {
                "deviceId": "C271111EC0AB",
                "deviceType": "Meter",
                "hubDeviceId": "FA7310762361",
                "humidity": 52,
                "temperature": 26.1
            },
            "message": "success"
        }"""),
    ),
    ReqResPair(
        request=FakeRequest(path='/v1.1/devices/E2F6032048AB/status'),
        response=FakeReponse(data=b"""{
            "statusCode": 100,
            "body": {
                "deviceId": "E2F6032048AB",
                "deviceType": "Curtain",
                "hubDeviceId": "FA7310762361",
                "calibrate": true,
                "group": false,
                "moving": false,
                "slidePosition": 0
            },
            "message": "success"
        }""")
    )
])
def test_validate_response(openapi: OpenAPI, pair: ReqResPair):
    """
    Test a number of known valid responses
    """
    openapi.validate_response(pair.request, pair.response)
