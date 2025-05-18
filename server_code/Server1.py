import anvil.users
import anvil.files
from anvil.files import data_files
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables

@anvil.server.callable
def submit(name):
  print("Hello, " + name + "!")

@anvil.server.callable
def set(key, value):
  """Set key-value pair; update if key exists, insert if new."""
  row = app_tables.data.get(key=key)
  if row:
    row['value'] = value
  else:
    app_tables.data.add_row(key=key, value=value)
  return "Saved"

@anvil.server.callable
def get(key):
  """Get value for a single key."""
  row = app_tables.data.get(key=key)
  return row['value'] if row else None

@anvil.server.callable
def get_all():
  """Return all entries as a dict."""
  return {row['key']: row['value'] for row in app_tables.data.search()}

@anvil.server.callable
def read(fn):
  with open(data_files[fn]) as f:
    text = f.read()
  return text

@anvil.server.callable
def write(fn,c):
  with data_files.editing(fn) as path:
    # path is now a string path on the filesystem. We can write to it with normal Python tools.
    # For example:
    with open(path, "w+") as f:
      f.write(c)
