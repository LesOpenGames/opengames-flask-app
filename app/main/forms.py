from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, SportLevel, CollectiveSportType, RacketSportType, RolesType

class PostForm(FlaskForm):
    post = TextAreaField(_l('Post Body'), validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField(_l('Publish'))

class EditTeamForm(FlaskForm):
    teamname = StringField(_l('Team Name'), validators=[DataRequired()])
    #sportlevel = RadioField(_('Sport Level'), coerce=int, choices=[(0, _('Easy')), (1, _('Tough')) ] )
    #collsport = RadioField(_('Racket Sport'), coerce=int, choices=[(0, _('Flag')), (1, _('Handball')) ] )
    #racksport = RadioField(_('Collective Sport'), coerce=int, choices=[(0, _('PingPong')), (1, _('Badmington')) ] )
    sportlevel = RadioField(_('Sport Level'), coerce=int, choices=[(int(SportLevel.EASY), _('Easy')), (int(SportLevel.TOUGH), _('Tough')) ] )
    collsport = RadioField(_('Racket Sport'), coerce=int, choices=[(int(CollectiveSportType.FLAG), _('Flag')), (int(CollectiveSportType.HAND), _('Handball')) ] )
    racksport = RadioField(_('Collective Sport'), coerce=int, choices=[(int(RacketSportType.PINGPONG), _('PingPong')), (int(RacketSportType.BADMINGTON), _('Badmington')) ] )
    submit = SubmitField(_l('Validate'))

class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About Me'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Change Profile'))
    # New constructor with param, called in routes.py       
    def __init__(self, original_username='', *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
    # Username validator, preventing allready used username
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))
