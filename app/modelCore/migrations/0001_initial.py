# Generated by Django 4.0.5 on 2022-09-15 06:25

import ckeditor_uploader.fields
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
                ('is_apply_servant', models.BooleanField(default=False)),
                ('is_passed', models.BooleanField(default=False)),
                ('is_servant_passed', models.BooleanField(default=False)),
                ('is_home', models.BooleanField(default=False)),
                ('home_hour_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('home_half_day_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('home_one_day_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('is_hospital', models.BooleanField(default=False)),
                ('hospital_hour_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('hospital_half_day_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('hospital_one_day_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('about_me', models.TextField(blank=True, default='', null=True)),
                ('is_continuous_time', models.BooleanField(default=True)),
                ('is_continuous_start_time', models.FloatField(blank=True, default=0, null=True)),
                ('is_continuous_end_time', models.FloatField(blank=True, default=24, null=True)),
                ('background_image', models.ImageField(blank=True, null=True, upload_to=modelCore.models.image_upload_handler)),
                ('ATMInfoBankCode', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('ATMInfoBranchBankCode', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('ATMInfoAccount', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AssistancePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('body', ckeditor_uploader.fields.RichTextUploadingField()),
                ('create_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('body', ckeditor_uploader.fields.RichTextUploadingField()),
                ('state', models.CharField(choices=[('draft', 'draft'), ('publish', 'publish')], max_length=10)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to=modelCore.models.image_upload_handler)),
                ('create_date', models.DateField(blank=True, null=True)),
                ('publish_date', models.DateField(blank=True, null=True)),
            ],
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
                ('state', models.CharField(choices=[('unTaken', '未承接'), ('unComplete', '未完成'), ('Complete', '已完成'), ('Canceled', '取消'), ('endEarly', '提早結束')], default='unTaken', max_length=10)),
                ('age', models.IntegerField(blank=True, default=0, null=True)),
                ('weight', models.IntegerField(blank=True, default=0, null=True)),
                ('disease_remark', models.CharField(blank=True, max_length=255, null=True)),
                ('conditions_remark', models.CharField(blank=True, max_length=255, null=True)),
                ('is_continuous_time', models.BooleanField(default=False)),
                ('is_taken', models.BooleanField(default=False)),
                ('is_open_for_search', models.BooleanField(default=False)),
                ('weekday', models.CharField(blank=True, max_length=100, null=True)),
                ('start_time', models.FloatField(blank=True, default=0, null=True)),
                ('end_time', models.FloatField(blank=True, default=24, null=True)),
                ('start_datetime', models.DateTimeField(blank=True, null=True)),
                ('end_datetime', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('taken_at', models.DateTimeField(auto_now=True, null=True)),
                ('emergencycontact_name', models.CharField(blank=True, max_length=100, null=True)),
                ('emergencycontact_relation', models.CharField(blank=True, max_length=100, null=True)),
                ('emergencycontact_phone', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('newebpay_cityname', models.CharField(blank=True, max_length=255, null=True)),
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
                ('remark', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MonthSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_date', models.DateField(null=True)),
                ('month_revenue', models.IntegerField(default=0)),
                ('month_cancel_amount', models.IntegerField(default=0)),
                ('month_pay_amount', models.IntegerField(default=0)),
                ('month_refound_amount', models.IntegerField(default=0)),
                ('month_platform_revenue', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('unPaid', '未付款'), ('paid', '已付款'), ('canceled', '已取消')], default='unPaid', max_length=10)),
                ('work_hours', models.FloatField(blank=True, default=0, null=True)),
                ('base_money', models.IntegerField(blank=True, default=0, null=True)),
                ('platform_percent', models.FloatField(blank=True, default=0, null=True)),
                ('platform_money', models.IntegerField(blank=True, default=0, null=True)),
                ('total_money', models.IntegerField(blank=True, default=0, null=True)),
                ('start_datetime', models.DateTimeField(blank=True, null=True)),
                ('end_datetime', models.DateTimeField(blank=True, null=True)),
                ('start_time', models.FloatField(blank=True, default=0, null=True)),
                ('end_time', models.FloatField(blank=True, default=24, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('refund_money', models.IntegerField(blank=True, default=0, null=True)),
                ('refund_apply_date', models.DateTimeField(auto_now=True, null=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='case_orders', to='modelCore.case')),
                ('servant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='servant_orders', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('remark', models.CharField(blank=True, max_length=150, null=True)),
                ('is_increase_price', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserWeekDayTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.CharField(choices=[('0', 'Sunday'), ('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday')], max_length=1)),
                ('start_time', models.FloatField(blank=True, default=0, null=True)),
                ('end_time', models.FloatField(blank=True, default=24, null=True)),
                ('start_time_hour', models.IntegerField(blank=True, default=8, null=True)),
                ('start_time_min', models.IntegerField(blank=True, default=0, null=True)),
                ('end_time_hour', models.IntegerField(blank=True, default=17, null=True)),
                ('end_time_min', models.IntegerField(blank=True, default=0, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='user_weekday', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MerchantID', models.CharField(blank=True, max_length=255, null=True)),
                ('MerchantHashKey', models.CharField(blank=True, max_length=255, null=True)),
                ('MerchantIvKey', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserServiceShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('increase_percent', models.FloatField(blank=True, default=0, null=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='service_ships', to='modelCore.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='ship_services', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserServiceLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transfer_fee', models.IntegerField(blank=True, default=0, null=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='modelCore.city')),
                ('county', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='modelCore.county')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='user_locations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserLicenseShipImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=modelCore.models.image_upload_handler)),
                ('isPassed', models.BooleanField(default=False)),
                ('license', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='license_image_ships', to='modelCore.license')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_license_images', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(blank=True, max_length=100, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.language')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='user_languages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TempCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('county', models.CharField(blank=True, max_length=100, null=True)),
                ('care_type', models.CharField(choices=[('home', '居家照顧'), ('hospital', '醫院看護')], default='', max_length=10)),
                ('name', models.CharField(default='', max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1)),
                ('state', models.CharField(choices=[('unTaken', '未承接'), ('unComplete', '未完成'), ('Complete', '已完成'), ('Canceled', '取消'), ('endEarly', '提早結束')], default='unTaken', max_length=10)),
                ('age', models.IntegerField(blank=True, default=0, null=True)),
                ('weight', models.IntegerField(blank=True, default=0, null=True)),
                ('disease_remark', models.CharField(default='', max_length=255)),
                ('conditions_remark', models.CharField(default='', max_length=255)),
                ('is_booking', models.BooleanField(default=False)),
                ('is_continuous_time', models.BooleanField(default=False)),
                ('is_taken', models.BooleanField(default=False)),
                ('is_open_for_search', models.BooleanField(default=False)),
                ('body_condition', models.CharField(blank=True, max_length=255, null=True)),
                ('disease', models.CharField(blank=True, max_length=255, null=True)),
                ('service', models.CharField(blank=True, max_length=255, null=True)),
                ('increase_service', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(default='', max_length=255)),
                ('tranfer_info', models.CharField(default='', max_length=255)),
                ('weekday', models.CharField(blank=True, max_length=100, null=True)),
                ('start_time', models.FloatField(blank=True, default=0, null=True)),
                ('end_time', models.FloatField(blank=True, default=24, null=True)),
                ('start_datetime', models.DateTimeField(blank=True, null=True)),
                ('end_datetime', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('emergencycontact_name', models.CharField(default='', max_length=100)),
                ('emergencycontact_relation', models.CharField(default='', max_length=100)),
                ('emergencycontact_phone', models.CharField(default='', max_length=10)),
                ('servant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='servant_tempcase', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
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
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='case_reviews', to='modelCore.case')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='order_reviews', to='modelCore.order')),
                ('servant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='servant_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PayInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PaymentType', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('MerchantID', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('OrderInfoMerchantOrderNo', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('OrderInfoTradeDate', models.DateTimeField(null=True)),
                ('OrderInfoTradeNo', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('OrderInfoTradeAmt', models.IntegerField(default=0, null=True)),
                ('OrderInfoPaymentType', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('OrderInfoPayTime', models.DateTimeField(null=True)),
                ('OrderInfoTradeStatus', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('EscrowBank', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('AuthBank', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('Auth', models.CharField(blank=True, default='', max_length=6, null=True)),
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
            name='OrderWeekDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.CharField(choices=[('0', 'Sunday'), ('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday')], max_length=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_weekdays', to='modelCore.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderIncreaseService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('increase_percent', models.FloatField(blank=True, default=0, null=True)),
                ('increase_money', models.IntegerField(blank=True, default=0, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_increase_services', to='modelCore.order')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.service')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_this_message_only_case', models.BooleanField(default=False)),
                ('content', models.TextField(blank=True, default='', null=True)),
                ('create_at', models.DateTimeField(auto_now=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=modelCore.models.image_upload_handler)),
                ('is_read_by_other_side', models.BooleanField(default=False)),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='modelCore.case')),
                ('chatroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatroom_messages', to='modelCore.chatroom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatroomUserShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chatroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelCore.chatroom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CaseServiceShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='case_services', to='modelCore.case')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelCore.service')),
            ],
        ),
        migrations.CreateModel(
            name='CaseDiseaseShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='case_diseases', to='modelCore.case')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelCore.diseasecondition')),
            ],
        ),
        migrations.CreateModel(
            name='CaseBodyConditionShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelCore.bodycondition')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='case_body_conditions', to='modelCore.case')),
            ],
        ),
        migrations.AddField(
            model_name='case',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='modelCore.city'),
        ),
        migrations.AddField(
            model_name='case',
            name='county',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='modelCore.county'),
        ),
        migrations.AddField(
            model_name='case',
            name='servant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='servant_cases', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='case',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='BlogPostCategoryShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ship_posts', to='modelCore.blogcategory')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ship_categories', to='modelCore.blogpost')),
            ],
        ),
    ]
