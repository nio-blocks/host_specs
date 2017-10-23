HostSpecs
===========
Get general specifications of the nio instance host.

Properties
----------
- **menu**: Flags for turning off/on various specs.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: An attribute is added for each specification read. Attribute names are the menu name followed by an underscore and then then specific specification.

Commands
--------
- **Hardware Architecture**: Returns the hardware system architecture.
- **Hardware Platform**: Returns the full platform information, including OS type, version, distribution in addition to hardware architecture.
- **OS Version**: Returns the operating system version.
- **OS Distribution**: Returns the operating system distribution.
- **OS Type**: Returns the operating system type.
- **Python Information**: Returns information regarding the running python version.  This includes the compiler, version, implementation type, and architecture.
- **Processor Type**: Returns the processor type and number of cores.

Dependencies
--------
psutil

Output Examples
---------------
When reading 'Python Information':
```
{
  'python': {
    'compiler': 'GCC 4.9.2',
    'version': '3.5.2',
    'implementation': 'CPython',
    'architecture': 64
  }
}
```

When reading 'Hardware Platform':
```
{
  'platform': 'Linux-4.9.49-moby-x86_64-with-debian-8.7'
}
```

When reading 'Processor Type':
```
{
  'cores': 4,
  'processor': ' Intel(R) Core(TM) i7-4770HQ CPU @ 2.20GHz'
}
```
