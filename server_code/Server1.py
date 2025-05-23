import anvil.users
import anvil.files
from anvil.files import data_files
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
import datetime
import anvil.email

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

@anvil.server.route("/files/:fn")
def get_file(fn, **params):
  with open(data_files['pages/'+fn]) as f:
    text = f.read()
  return anvil.server.HttpResponse(200,text)
@anvil.server.route("/forms/:fn")
def get_form(fn, **params):
  return anvil.server.FormResponse(fn)
@anvil.server.callable
def email(name, email, feedback):
  app_tables.feed.add_row(
                   subject="Feedback from {}".format(name),
                   text=f"""FeedBack:
                   Name: {name}
                   Email address: {email}
                   Feedback:{feedback}
                   """)