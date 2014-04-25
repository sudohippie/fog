# Fog
Fog is an open-source cross-platform Git styled tool to upload, download and remove files from remote cloud drives.
It is written in Python.

## Status
|Branch|Build|
|------|-----|
|master|[![Build Status](https://travis-ci.org/sudohippie/fog.svg?branch=master)](https://travis-ci.org/sudohippie/fog)|
|stable|[![Build Status](https://travis-ci.org/sudohippie/fog.svg?branch=stable)](https://travis-ci.org/sudohippie/fog)|

## Usage
Commands are very similar to git. The ``help`` command provides information on available commands.

```
$ python fog/fog.py help
```

## Prerequisites
* ``python >= 2.7`` (tested with version 2.7)

Need a few [pip](http://www.pip-installer.org/en/latest/reference/pip.html) installations,

* ``google-api-python-client`` ([details](https://developers.google.com/api-client-library/python/start/installation))

See [requirements](requirements.txt) document for exact versions.

## Installation
To install simply clone this repository.

```
$ git clone https://github.com/sudohippie/fog
$ cd fog
```

## Documentation
Documentation is available on the [Wiki](https://github.com/sudohippie/fog/wiki).

## Author
Raghav Sidhanti

## License
The MIT License. See [LICENSE](LICENSE) for details.
