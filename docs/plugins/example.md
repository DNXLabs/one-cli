---
layout: default
title: Example
parent: Plugins
nav_order: 1
---

#### Plugin Example

`~/.one/plugins/first_plugin/__init__.py`
```python
import click
from one.one import cli

def __init__():
    cli.add_command(my_plugin)

@click.command(name='my_plugin', help='My plugin command')
def my_plugin():
    click.echo('It works!')
```