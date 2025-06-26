from rest_framework.serializers import ModelSerializer, ValidationError
from apps.models import Contact, Debt


class ContactModelSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = 'id','phone_number', 'fullname'



    def save(self, **kwargs):
        data = self.data
        data['user'] = self.context['request'].user
        Contact.objects.create(**data)

class DebtModelSerializer(ModelSerializer):
    class Meta:
        model = Debt
        fields = "debt_amount", "description","due_date","is_my_debt"
        read_only_fields = "is_paid" ,
    def save(self, **kwargs):
        data = self.data
        data['contact_id'] = self.context['request'].parser_context.get('kwargs').get('pk')
        Debt.objects.create(**data)



class ContactUpdateSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'user', 'fullname', 'phone_number', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def validate_phone_number(self, value):
        if len(value) < 9:
            raise ValidationError("Noto'g'ri telefon raqam!")
        return value