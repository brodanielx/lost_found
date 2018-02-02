import django_tables2 as tables
from .models import Contact

class ContactTable(tables.Table):
    full_name = tables.TemplateColumn('<a href="/contacts/contact/{{record.id}}">{{record.full_name}}</a>')
    edit = tables.TemplateColumn('<a href="/contacts/editcontact/{{record.id}}"><i class="fa fa-pencil-square-o fa-lg" aria-hidden="true"></i></a>', orderable=False, exclude_from_export=True)
    created_at = tables.DateColumn(format='n/j/y')
    updated_at = tables.DateColumn(format='n/j/y')
    gender = tables.TemplateColumn('<p>{{record.gender}}</p>')
    added_by = tables.TemplateColumn('<p>{{record.added_by.first_name}} {{record.added_by.last_name}}</p>')
    class Meta:
        model = Contact
        fields = ('gender', 'full_name', 'phone_number_formated', 'email', 'zip_code', 'created_at', 'updated_at', 'added_by', 'edit')
        attrs = {
            'class': 'table table-hover table-striped',
            }
