| Branch | Coverage |
| --- | --- |
| Master | [![codecov](https://codecov.io/gh/CIMAC-CIDC/cidc-utils/branch/master/graph/badge.svg)](https://codecov.io/gh/CIMAC-CIDC/cidc-utils/branch/master/) |
| Staging | [![codecov](https://codecov.io/gh/CIMAC-CIDC/cidc-utils/branch/staging/graph/badge.svg)](https://codecov.io/gh/CIMAC-CIDC/cidc-utils/branch/staging/) |
### Introduction
A simple utility package for the CIDC tools, provides convenient shortcut methods for some of the common tasks. 


### Points of Interest

`from cidc_utils.requests import SmartFetch`

Imports an easy to use request class with automatic error handling and shortcut methods for common tasks.

`from cidc_utils.loghandler import StackdriverJsonFormatter`

This formatter can be used with pythons `logging` library to format log messages in a way that Stackdriver can understand and procses.

### Installation

`pip3 install http://github.com/CIMAC-CIDC/cidc-utils.git#egg=cidc_utils --user`
