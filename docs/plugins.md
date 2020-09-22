## Plugin System

To give better support for customization inside the CLI we created a `plugin system` that you can extend code, creating new commands and groups and even modify the existing ones.

All plugins need to be created inside ` ~/.one/plugins/*`

#### Folder Structure

```bash
└── plugins
    ├── __init__.py (empty file)
    └── my_plugin.py
```

#### Plugin Example

`~/.one/plugins/my_plugin.py`
```python
import click
from one.one import cli


def __init__():
    cli.add_command(my_plugin)


@click.command(name='my_plugin', help='My plugin command')
def my_plugin():
    click.echo('It works!')
```