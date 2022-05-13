"""Peewee migrations -- 001_init.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import datetime as dt
import peewee as pw
from decimal import ROUND_HALF_EVEN

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    @migrator.create_model
    class BannedUser(pw.Model):
        id = pw.BigIntegerField(primary_key=True)
        user_id = pw.BigIntegerField()
        ban_count = pw.IntegerField()
        banned_until = pw.DateTimeField()
        is_banned = pw.BooleanField(constraints=[SQL("DEFAULT False")], default=False)

        class Meta:
            table_name = "banned_users"

    @migrator.create_model
    class BaseModel(pw.Model):
        id = pw.AutoField()

        class Meta:
            table_name = "basemodel"

    @migrator.create_model
    class Bill(pw.Model):
        id = pw.IntegerField(primary_key=True)
        label = pw.CharField(max_length=255)
        status = pw.CharField(max_length=255, null=True)
        amount = pw.FloatField()
        user_id = pw.BigIntegerField()
        created_at = pw.DateTimeField()
        updated_at = pw.DateTimeField()

        class Meta:
            table_name = "bills"

    @migrator.create_model
    class User(pw.Model):
        id = pw.BigIntegerField(primary_key=True)
        username = pw.CharField(max_length=255, null=True)
        first_name = pw.CharField(max_length=255)
        last_name = pw.CharField(max_length=255, null=True)
        language = pw.CharField(constraints=[SQL("DEFAULT 'ru'")], default='ru', max_length=255)
        time_zone = pw.CharField(constraints=[SQL("DEFAULT 'Europe/Kiev'")], default='Europe/Kiev', max_length=255)
        is_vip = pw.BooleanField(constraints=[SQL("DEFAULT False")], default=False)
        is_admin = pw.BooleanField(constraints=[SQL("DEFAULT False")], default=False)
        settings = pw.CharField(max_length=255, null=True)
        created_at = pw.DateTimeField()
        referal_id = pw.BigIntegerField(null=True)
        banned_until = pw.DateTimeField(null=True)
        ban_count = pw.IntegerField(constraints=[SQL("DEFAULT 0")], default=0)
        is_banned = pw.BooleanField(constraints=[SQL("DEFAULT False")], default=False)

        class Meta:
            table_name = "users"

    @migrator.create_model
    class Reminder(pw.Model):
        id = pw.BigIntegerField(primary_key=True)
        user = pw.ForeignKeyField(backref='reminders', column_name='user_id', field='id', model=migrator.orm['users'])
        text = pw.CharField(max_length=255)
        date = pw.DateTimeField()
        is_repeat = pw.BooleanField(constraints=[SQL("DEFAULT False")], default=False)
        repeat_count = pw.IntegerField(constraints=[SQL("DEFAULT -1")], default=-1, null=True)
        curr_repeat = pw.IntegerField(constraints=[SQL("DEFAULT 1")], default=1)
        repeat_until = pw.DateTimeField(null=True)
        repeat_range = pw.CharField(constraints=[SQL("DEFAULT 'day'")], default='day', max_length=255)
        next_date = pw.DateTimeField()
        is_reminded = pw.BooleanField(constraints=[SQL("DEFAULT False")], default=False)
        is_deleted = pw.BooleanField(constraints=[SQL("DEFAULT False")], default=False)

        class Meta:
            table_name = "reminders"



def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

    migrator.remove_model('users')

    migrator.remove_model('reminders')

    migrator.remove_model('bills')

    migrator.remove_model('basemodel')

    migrator.remove_model('banned_users')
