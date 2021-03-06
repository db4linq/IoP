"""Peewee migrations: ::

    > Model = migrator.orm['name']

    > migrator.sql(sql)
    > migrator.python(func, *args, **kwargs)
    > migrator.create_model(Model)
    > migrator.remove_model(Model, cascade=True)
    > migrator.add_fields(Model, **fields)
    > migrator.change_fields(Model, **fields)
    > migrator.remove_fields(Model, *field_names, cascade=True)
    > migrator.rename_field(Model, old_field_name, new_field_name)
    > migrator.rename_table(Model, new_table_name)
    > migrator.add_index(Model, *col_names, unique=False)
    > migrator.drop_index(Model, *col_names)
    > migrator.add_not_null(Model, *field_names)
    > migrator.drop_not_null(Model, *field_names)
    > migrator.add_default(Model, field_name, default)

"""

import datetime as dt
import peewee as pw


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    @migrator.create_model
    class KeyChain(pw.Model):
        secret = pw.TextField()
        message = pw.TextField()
        application = pw.CharField(max_length=255)

    @migrator.create_model
    class MailAccount(pw.Model):
        account = pw.CharField(max_length=255)
        transport = pw.CharField(default='smtp', max_length=255)
        server = pw.CharField(max_length=255)
        encryption = pw.CharField(default='ssl', max_length=255)
        port = pw.IntegerField(default=465)
        daemon = pw.BooleanField(default=False)
        password = pw.ForeignKeyField(db_column='password_id', rel_model=KeyChain, to_field='id')

    @migrator.create_model
    class Person(pw.Model):
        email = pw.CharField(max_length=255)
        name = pw.CharField(max_length=255)
        wizard = pw.BooleanField(default=False)

    @migrator.create_model
    class Plant(pw.Model):
        name = pw.CharField(max_length=255)
        location = pw.CharField(max_length=255)
        species = pw.CharField(max_length=255)
        interval = pw.IntegerField()
        person = pw.ForeignKeyField(db_column='person_id', rel_model=Person, to_field='id')
        role = pw.CharField(default='master', max_length=255)
        ip = pw.CharField(max_length=255)
        localhost = pw.BooleanField(default=False)
        created_at = pw.DateTimeField()
        sat_streak = pw.IntegerField()

    @migrator.create_model
    class PlantNetworkStatus(pw.Model):
        name = pw.CharField(max_length=255)

    @migrator.create_model
    class PlantNetworkUptime(pw.Model):
        plant = pw.ForeignKeyField(db_column='plant_id', rel_model=Plant, to_field='id')
        status = pw.ForeignKeyField(db_column='status_id', rel_model=PlantNetworkStatus, to_field='id')
        overall = pw.FloatField()
        current = pw.FloatField()

    @migrator.create_model
    class Sensor(pw.Model):
        model = pw.CharField(max_length=255)
        name = pw.CharField(max_length=255, unique=True)
        unit = pw.CharField(max_length=255)
        min_value = pw.FloatField()
        max_value = pw.FloatField()
        persistant_offset = pw.FloatField(default=1)
        persistant_hold = pw.IntegerField(default=2016)

    @migrator.create_model
    class SensorData(pw.Model):
        value = pw.FloatField()
        plant = pw.ForeignKeyField(db_column='plant_id', rel_model=Plant, to_field='id')
        sensor = pw.ForeignKeyField(db_column='sensor_id', rel_model=Sensor, to_field='id')
        persistant = pw.BooleanField(default=False)
        created_at = pw.DateTimeField()

    @migrator.create_model
    class SensorHardware(pw.Model):
        label = pw.CharField(max_length=255)
        function = pw.CharField(default='generic', max_length=255)
        last_execution = pw.DateTimeField(null=True)

    @migrator.create_model
    class SensorHardwareConnector(pw.Model):
        sensor = pw.ForeignKeyField(db_column='sensor_id', rel_model=Sensor, to_field='id')
        hardware = pw.ForeignKeyField(db_column='hardware_id', rel_model=SensorHardware, to_field='id')

    @migrator.create_model
    class SensorSatisfactionLevel(pw.Model):
        label = pw.CharField(max_length=255)
        name_color = pw.CharField(max_length=255)
        hex_color = pw.CharField(max_length=255, null=True)

    @migrator.create_model
    class SensorDangerMessage(pw.Model):
        plant = pw.ForeignKeyField(db_column='plant_id', rel_model=Plant, to_field='id')
        sensor = pw.ForeignKeyField(db_column='sensor_id', rel_model=Sensor, to_field='id')
        level = pw.ForeignKeyField(db_column='level_id', rel_model=SensorSatisfactionLevel, to_field='id')
        message = pw.TextField()
        value = pw.FloatField()
        sent = pw.BooleanField(default=False)
        sent_time = pw.DateTimeField(null=True)
        created_at = pw.DateTimeField()

    @migrator.create_model
    class SensorCount(pw.Model):
        sensor = pw.ForeignKeyField(db_column='sensor_id', rel_model=Sensor, to_field='id')
        plant = pw.ForeignKeyField(db_column='plant_id', rel_model=Plant, to_field='id')
        level = pw.ForeignKeyField(db_column='level_id', rel_model=SensorSatisfactionLevel, to_field='id')
        count = pw.IntegerField()

    @migrator.create_model
    class SensorSatisfactionValue(pw.Model):
        sensor = pw.ForeignKeyField(db_column='sensor_id', rel_model=Sensor, to_field='id')
        plant = pw.ForeignKeyField(db_column='plant_id', rel_model=Plant, to_field='id')
        level = pw.ForeignKeyField(db_column='level_id', rel_model=SensorSatisfactionLevel, to_field='id')
        inherited = pw.BooleanField(default=False)
        min_value = pw.FloatField(default=0, null=True)
        max_value = pw.FloatField(default=1, null=True)

    @migrator.create_model
    class SensorStatus(pw.Model):
        sensor = pw.ForeignKeyField(db_column='sensor_id', rel_model=Sensor, to_field='id')
        plant = pw.ForeignKeyField(db_column='plant_id', rel_model=Plant, to_field='id')
        level = pw.ForeignKeyField(db_column='level_id', rel_model=SensorSatisfactionLevel, to_field='id')
        status = pw.BooleanField(default=False)



def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

    migrator.remove_model('sensorstatus')

    migrator.remove_model('sensorsatisfactionvalue')

    migrator.remove_model('sensorcount')

    migrator.remove_model('sensordangermessage')

    migrator.remove_model('sensorsatisfactionlevel')

    migrator.remove_model('sensorhardwareconnector')

    migrator.remove_model('sensorhardware')

    migrator.remove_model('sensordata')

    migrator.remove_model('sensor')

    migrator.remove_model('plantnetworkuptime')

    migrator.remove_model('plantnetworkstatus')

    migrator.remove_model('plant')

    migrator.remove_model('person')

    migrator.remove_model('mailaccount')

    migrator.remove_model('keychain')
