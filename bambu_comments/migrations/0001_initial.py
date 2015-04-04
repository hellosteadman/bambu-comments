# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('website', models.URLField(max_length=255, null=True, blank=True)),
                ('email', models.EmailField(max_length=255, db_index=True)),
                ('sent', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('approved', models.BooleanField(default=False, db_index=True)),
                ('spam', models.BooleanField(default=False, db_index=True)),
                ('body', models.TextField()),
                ('object_id', models.PositiveIntegerField(db_index=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('-sent',),
                'db_table': 'comments_comment',
                'get_latest_by': 'sent',
            },
        ),
    ]
