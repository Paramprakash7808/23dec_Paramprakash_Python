from django.contrib.auth.models import Group

groups = ['Admin', 'Author', 'Reader']
for group in groups:
    Group.objects.get_or_create(name=group)

print("Roles (Groups) created successfully.")
