# OpenAPI Specification for SwitchBot Home Automation

[SwitchBot has human-readable documentation for its API](https://github.com/OpenWonderLabs/SwitchBotAPI). Unfortunately this doesn't include a machine-readable API specification, which is why I've adapted their documentation into OpenAPI.
Using this, you can generate API clients, validate your requests, and more easily explore the available endpoints.

### [Get the spec here](https://github.com/multimeric/SwitchBotOpenAPI/blob/main/openapi.yml)

## Current Status

* `/v1.1/devices` (list devices) is fully described
* `/v1.1/devices/{deviceId}/status` (device status) is fully described
* `/v1.1/devices/{deviceId}/commands` (contorl devices) is not described