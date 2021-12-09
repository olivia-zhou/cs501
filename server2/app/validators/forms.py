from wtforms import Form, StringField, validators, ValidationError, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.validators.base import BaseForm
from app.models.command import Command 
from app.models.agent import Agent
from app.libs.error_code import NotFound 

class AddCmdForm(BaseForm): 
    cmd = StringField(validators=[DataRequired(), Length(min=1, max=100)])
    agent_id = IntegerField(validators=[DataRequired()])
    #校验agent_id是否存在
    def validate_agent_id(self, field):
        print("field.data:",field.data)
        if not Agent.query.filter_by(id=field.data).first():
            raise NotFound('agent not found')

class LoginForm(BaseForm):
    username = StringField(validators=[DataRequired(), Length(min=1, max=100)])
    password = StringField(validators=[DataRequired(), Length(min=1, max=100)])


class PingForm(BaseForm):
    host_name = StringField(validators=[DataRequired()])
    user_login_name = StringField(validators=[DataRequired()])
    intergrity = StringField(validators=[DataRequired()])
    ip = StringField(validators=[DataRequired()])
    session_key = StringField(validators=[DataRequired()])

class ResultForm(BaseForm):
    cmd_id = StringField(validators=[DataRequired()])
    result = StringField(validators=[DataRequired()])

    #校验cmd_id是否存在
    def validate_cmd_id(self, field):
        cmd = Command.query.filter_by(id=field.data).first()
        if not cmd:
            raise NotFound('cmd_id is not found')



