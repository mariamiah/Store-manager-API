class User(object):
    def __init__(self, employee_id, employee_name, email, gender, username,
                 password, role):
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.email = email
        self.gender = gender
        self.username = username
        self.password = password
        self.role = role

    def check_role(self):
        if self.role == "admin":
            return "Is_admin"
        return "Is_attendant"
