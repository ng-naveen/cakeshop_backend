# Generated by Django 5.1.4 on 2024-12-13 16:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Occasion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('weight', models.CharField(max_length=50)),
                ('shape', models.CharField(choices=[('round', 'round'), ('square', 'square'), ('heart', 'heart')], default='round', max_length=10)),
                ('layers', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], default='1', max_length=10)),
                ('price', models.FloatField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='cake_images/')),
                ('occasion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.occasion')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('address', models.CharField(max_length=250)),
                ('matter', models.CharField(max_length=250)),
                ('status', models.CharField(choices=[('order-placed', 'order-placed'), ('shipped', 'shipped'), ('delivered', 'delivered'), ('returned', 'returned'), ('cancelled', 'cancelled')], default='order-placed', max_length=50)),
                ('cake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cake')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('review_text', models.CharField(max_length=250)),
                ('cake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cake')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('cake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cake')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'cake')},
            },
        ),
    ]
