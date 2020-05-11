from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class BlockChainInput(FlaskForm):
	company_name = StringField('Company_Name', validators=[DataRequired()])
	quantity = IntegerField('Quantity', validators=[DataRequired()])

	def validate_quantity(form, field):
		try:
			field.data = IntegerField(field)
		except TypeError: 
			raise ValidationError('Quantity must be an integer')


	submit = SubmitField('Enter')
	
	    