
# Code instrumentation

The Python implementation of the protocol relies on the automatic code
instrumentation that is implemented through the
[command](#gsp.io.command.command) function decorator. This decorator
registers all necessary information when a method is called and offers
convenient conversion functions. This works by inspecting the declared
type of a method (using [function
annotations](https://peps.python.org/pep-3107/)) and checking of the
provided type has the right type. If this is not the case, the command
search for a converter among those registered.

```python tabs="Code instrumentation | Output" exec="true" source="tabbed-left" result="pycon"
import gsp

@gsp.io.register("float", "int")
def float_to_int(value): return int(value)

class Foo(gsp.Object):
    @gsp.io.command("CREATE")
    def __init__(self, value : int):
        gsp.Object.__init__(self)
        self.value = value
        
foos = Foo(1), Foo(2)
print(gsp.io.queue("active"))
```

## Command related functions

::: gsp.io.command.queue

::: gsp.io.command.record

::: gsp.io.command.command

## Conversion related functions

::: gsp.io.convert.register

::: gsp.io.convert.unregister

::: gsp.io.convert.convert



