# Generated by Django 3.0.5 on 2025-01-22 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
        ('insurance', '0004_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaimRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Pending', max_length=100)),
                ('claim_date', models.DateField(auto_now=True)),
                ('Claim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance.Policy')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_name', models.CharField(max_length=200)),
                ('claim_amount', models.PositiveIntegerField()),
                ('premium', models.PositiveIntegerField()),
                ('claim_date', models.DateField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance.Category')),
            ],
        ),
    ]
