from ._anvil_designer import feedTemplate
from anvil import *
import anvil.server

import re

class feed(feedTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def is_valid_email(self, email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

  def submit_click(self, **event_args):
    name = self.name.text.strip()
    email = self.email.text.strip()
    feedback = self.feedback.text.strip()

    if not name or not email or not feedback:
      alert("All fields are required.", title="Missing Information")
      return

    if not self.is_valid_email(email):
      alert("Please enter a valid email address.", title="Invalid Email")
      return

    with Notification("Sending feedback...", timeout=None):
      anvil.server.call('email', name, email, feedback)

    alert("Feedback sent successfully!", title="Thank You")

    # Clear the form fields
    self.name.text = ""
    self.email.text = ""
    self.feedback.text = ""
