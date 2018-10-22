class User(object):
    def __init__(self, **kwargs):
        self.employee_id = kwargs['employee_id']
        self.employee_name = kwargs['employee_name']
        self.email = kwargs['email']
        self.gender = kwargs['gender']
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.role = kwargs['role']
