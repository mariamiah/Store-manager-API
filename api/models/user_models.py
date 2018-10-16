class StoreEmployee(object):
    def __init__(self, employee_id, employee_name, email, gender):
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.email = email
        self.gender = gender


class Admin(StoreEmployee):
    def __init__(self, employee_id, employee_name, email, gender,
                 adminUser_name, admin_password):
        super().__init__(employee_id, employee_name, email, gender)
        self.adminUser_name = adminUser_name
        self.admin_password = admin_password


class Attendant(StoreEmployee):
    def __init__(self, employee_id, employee_name, email, gender,
                 attendantUser_name, attendant_password):
        super().__init__(employee_id, employee_name, email, gender)
        self.attendantUser_name = attendantUser_name
        self.attendant_password = attendant_password
