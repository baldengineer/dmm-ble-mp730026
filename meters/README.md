# Quick setup
* Create meter as a class, inheriting DMM from parent
```python
import asyncio
from .. import DMM

class ModelNumber(DMM):
    def __init__(self, address):
        DMM.__init__(self, address)

        self.model = "Mfg Model"

    async def run():
        # Do your magic here.
```

This will give you access to self.unit_strings and self.mode_strings as well as initialize the expected values needed to be sent to the websocket

