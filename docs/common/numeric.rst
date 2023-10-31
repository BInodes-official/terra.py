.. numeric:

Numeric Types
=============

.. autoclass:: terra_classic_sdk.core.numeric.Numeric
    :members:

Integers
--------

Terra Classic SDK uses Python's native ``int`` type to capture both native numbers like ``uint8``, as well
as Cosmos SDK's ``sdk.Int`` which is normally coerced into a string as it must be passed in JSON format.
The Python's ``int`` provides support for BigNumber implementation for artihmetic operations.

.. warning::
    It is possible to introduce numbers larger than 256-bit precision allowed by the Terra Classic blockchain but
    they will result in an error when processing.


Decimals
--------

.. autoclass:: terra_classic_sdk.core.Dec
    :members:
