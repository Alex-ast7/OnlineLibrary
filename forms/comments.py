from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired


class AddCommentForm(FlaskForm):
    text = StringField("Text", validators=[DataRequired()])
    star1 = BooleanField()
    star2 = BooleanField()
    star3 = BooleanField()
    star4 = BooleanField()
    star5 = BooleanField()
    submit = SubmitField("Оставить отзыв")