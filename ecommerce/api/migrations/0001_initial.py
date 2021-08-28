from django.db import migrations
from ..user.models import CustomUser


class Migration(migrations.Migration):

    def seed_data(apps, schema_editor):
        user = CustomUser(name="divyanshu",
                          email="divyanshu@gmail.com",
                          is_staff=True,
                          is_superuser=True,
                          gender='Male')

        user.set_password("12345")
        user.save()

    dependencies = [

    ]

    operations = [
        migrations.RunPython(seed_data),
    ]