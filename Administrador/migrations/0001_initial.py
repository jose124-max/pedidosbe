# Generated by Django 5.0 on 2023-12-24 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id_administrador', models.AutoField(primary_key=True, serialize=False)),
                ('telefono', models.CharField(blank=True, max_length=10, null=True)),
                ('apellido', models.CharField(max_length=300)),
                ('nombre', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'administrador',
                'managed': False,
            },
        ),
    ]
