import django_tables2 as tables
from .models import Contact

class ContactByUserTable(tables.Table):
    full_name = tables.TemplateColumn('<a href="/contacts/contact/{{record.id}}">{{record.full_name}}</a>')
    edit = tables.TemplateColumn('<a href="/contacts/editcontact/{{record.id}}"><i class="fa fa-pencil-square-o fa-lg" aria-hidden="true"></i></a>', orderable=False)
    created_at = tables.DateColumn(format='n/j/y')
    class Meta:
        model = Contact
        fields = ('id', 'gender', 'full_name', 'phone_number_formated', 'email', 'created_at', 'edit')
        attrs = {
            'class': 'table table-hover',
            }
