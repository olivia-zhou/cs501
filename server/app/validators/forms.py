from wtforms import Form, StringField, validators, ValidationError, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class AddCmdForm(Form): 
    cmd = StringField(validators=[DataRequired(), Length(min=1, max=100)])
    agent_id = IntegerField(validators=[DataRequired()])

    def validate_agent_id(self, agent_id):
        if agent_id.data == 0:
            raise ValidationError('Agent ID is required')