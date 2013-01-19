from flask.ext.wtf import Form, TextField, PasswordField, validators


class LoginForm(Form):
    username = TextField('Usuario', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        if self.username.data != 'admin':
            self.username.errors.append('Nombre de usuario invalido')
            return False

        if self.password.data != 'xx':
            self.password.errors.append('Password Incorrecto')
            return False

        return True





