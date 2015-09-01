DESCRIPTION
===========

Bean fetcher is a simple utility to fetch jobs from beanstalk server.

INSTALLATION
============

Use python setuptools:

	# python setup.py install

USAGE
=====

	bean-fetcher [-c <configuration_path> ]

Default configuration is **/usr/local/etc/bean-fetcher.ini**

CONFIGURATION
=============

Here is a simple config:

```ini
[instance1]
host = 127.0.0.1
port = 11302
command = /usr/local/bin/some_command -h -t %%t
workers = 4
user = nobody

[instance2]
port = 11303
file = /path/to/file
tube = test
```

If host is omitted then 'localhost' is used. If port is omitted
then `11300` is used. If argument is `%t` then it is replaced by current date
in format `%Y-%m-%d`. If user is omitted then command is started without
user's changing. If tube is omitted then `default` tube is used.

TODO
====

- Add more options.
- Add errors handling.
- Add timeouts.
