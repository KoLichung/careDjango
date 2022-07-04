# Generated by Django 4.0.5 on 2022-07-04 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelCore.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone', models.CharField(max_length=10, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=modelCore.models.image_upload_handler)),
                ('line_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('is_servant', models.BooleanField(default=False)),
                ('rating', models.FloatField(blank=True, default=0, null=True)),
                ('is_home', models.BooleanField(default=False)),
                ('home_hour_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('home_half_day_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('home_one_day_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('is_hospital', models.BooleanField(default=False)),
                ('hospital_hour_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('hospital_half_day_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('hospital_one_day_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('about_me', models.TextField(blank=True, default='', null=True)),
                ('is_alltime_service', models.BooleanField(default=True)),
                ('background_image', models.ImageField(blank=True, null=True, upload_to=modelCore.models.image_upload_handler)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BodyCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('care_type', models.CharField(choices=[('home', '居家照顧'), ('hospital', '醫院看護')], default='', max_length=10)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1)),
                ('age', models.IntegerField(blank=True, default=0, null=True)),
                ('weight', models.IntegerField(blank=True, default=0, null=True)),
                ('disease_remark', models.CharField(blank=True, max_length=255, null=True)),
                ('conditions_remark', models.CharField(blank=True, max_length=255, null=True)),
                ('is_alltime_service', models.BooleanField(default=False)),
                ('is_taken', models.BooleanField(default=False)),
                ('is_open_for_search', models.BooleanField(default=False)),
                ('start_datetime', models.DateTimeField(blank=True, null=True)),
                ('end_datetime', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.city')),
            ],
        ),
        migrations.CreateModel(
            name='DiseaseCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('unPaid', '未付款'), ('paid', '已付款')], default='unPaid', max_length=10)),
                ('total_money', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelCore.case')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('is_increase_price', models.BooleanField(default=False)),
                ('increase_percent', models.FloatField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserWeekDayTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.CharField(choices=[('0', 'Sunday'), ('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday')], max_length=1)),
                ('start_time', models.IntegerField(blank=True, default=0, null=True)),
                ('end_time', models.IntegerField(blank=True, default=24, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserServiceShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserServiceLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tranfer_fee', models.IntegerField(blank=True, default=0, null=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.city')),
                ('county', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.county')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='service_locations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserLicenseShipImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=modelCore.models.image_upload_handler)),
                ('license', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelCore.license')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(max_length=100, unique=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.language')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='languages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SystemMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, default='', null=True)),
                ('create_at', models.DateTimeField(auto_now=True, null=True)),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='modelCore.case')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_offender_rating', models.FloatField(blank=True, default=0, null=True)),
                ('case_offender_comment', models.CharField(blank=True, max_length=255, null=True)),
                ('case_offender_rating_created_at', models.DateTimeField(blank=True, null=True)),
                ('servant_rating', models.FloatField(blank=True, default=0, null=True)),
                ('servant_comment', models.CharField(blank=True, max_length=255, null=True)),
                ('servant_rating_created_at', models.DateTimeField(blank=True, null=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelCore.case')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.order')),
                ('servant', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PayInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PaymentType', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('MerchantID', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('OrderInfoMerchantTradeNo', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('OrderInfoTradeDate', models.DateTimeField(null=True)),
                ('OrderInfoTradeNo', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('OrderInfoTradeAmt', models.IntegerField(default=0, null=True)),
                ('OrderInfoPaymentType', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('OrderInfoChargeFee', models.DecimalField(decimal_places=2, max_digits=9, null=True)),
                ('OrderInfoTradeStatus', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('CardInfoAuthCode', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('CardInfoGwsr', models.IntegerField(default=0, null=True)),
                ('CardInfoProcessDate', models.DateTimeField(null=True)),
                ('CardInfoAmount', models.IntegerField(default=0, null=True)),
                ('CardInfoCard6No', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('CardInfoCard4No', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.RESTRICT, to='modelCore.order')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, default='', null=True)),
                ('create_at', models.DateTimeField(auto_now=True, null=True)),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='modelCore.case')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CaseWeekDayTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.CharField(blank=True, choices=[('0', 'Sunday'), ('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday')], max_length=1, null=True)),
                ('start_time', models.IntegerField(blank=True, default=0, null=True)),
                ('end_time', models.IntegerField(blank=True, default=24, null=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.case')),
            ],
        ),
        migrations.CreateModel(
            name='CaseServiceShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.case')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.service')),
            ],
        ),
        migrations.CreateModel(
            name='CaseDiseaseShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.case')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.diseasecondition')),
            ],
        ),
        migrations.CreateModel(
            name='CaseBodyConditionShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_condition', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.bodycondition')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.case')),
            ],
        ),
        migrations.AddField(
            model_name='case',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.city'),
        ),
        migrations.AddField(
            model_name='case',
            name='county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.county'),
        ),
        migrations.AddField(
            model_name='case',
            name='servant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cases', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='case',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
    ]
