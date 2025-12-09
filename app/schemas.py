from marshmallow import Schema, fields, validates_schema, ValidationError

class BudgetSchema(Schema):
    income = fields.Float(required=True)
    monthly_bills = fields.Float(required=True)
    food = fields.Float(required=True)
    transport = fields.Float(required=True)
    subscriptions = fields.Float(required=True)
    miscellaneous = fields.Float(required=True)

    @validates_schema
    def validate_non_negative(self, data, **kwargs):
        for key, value in data.items():
            if value < 0:
                raise ValidationError(f"{key} cannot be negative", field_name=key)


class BudgetResponseSchema(BudgetSchema):
    id = fields.Int()
    updated_at = fields.DateTime()
    last_synced_at = fields.DateTime(allow_none=True)
