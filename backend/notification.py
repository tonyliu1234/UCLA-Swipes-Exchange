class Notification:
  def __init__(self, users, message):
    self.users = users
    self.message = message

  def belong_to_user(self, user):
    return user in self.users