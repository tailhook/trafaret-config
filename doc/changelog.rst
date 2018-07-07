Trafaret-config Changes by Release
==================================

v2.0.0
------

* breaking: trafaret >= 1.2.0 is only supported (previous versions may work)
* breaking: PyYAML >= 4.1 is only supported (previous versions may work)
* breaking feature: Variables like ``$this`` or ``${THIS}`` are substituted in
  all scalar in yaml file, if you relied on this kind of values present in the
  config verbatim, pass ``vars=None`` to config parser
* feature: Add ``--print-config-vars`` command-line argument to print variables
  used in specific config
