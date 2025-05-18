from ._anvil_designer import Form1Template
from anvil import *
import anvil.users
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Load existing value for key "name"
    existing = anvil.server.call('get', 'name')
    if existing:
      self.name.text = existing

  def submit_click(self, **event_args):
    value = self.name.text.strip()
    if not value:
      alert("Please enter a name.")
      return
    result = anvil.server.call('set', 'name', value)
    alert(result)
