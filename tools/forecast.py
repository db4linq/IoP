import pandas as pd
import numpy as np
import datetime
from models.sensor import SensorData
from models.sensor import SensorDataPrediction
from settings.debug import GRAPH
from sklearn.ensemble import ExtraTreesRegressor


class SensorDataForecast(object):
  def __init__(self):
    pass

  def show_graph(self, data_dates, data, prediction_dates, predictions):
    import matplotlib.pylab as plt

    index = pd.DatetimeIndex(data_dates)
    original = pd.Series(data, index=index)

    index = pd.DatetimeIndex(prediction_dates)
    predicted = pd.Series(predictions, index=index)

    plt.plot(original, color='red')
    plt.plot(predicted, color='blue')
    plt.show()

  def datetime_to_dict(self, array, field='date'):
    array['timestamp'] = []
    array['year'] = []
    array['month'] = []
    array['day'] = []
    array['hour'] = []
    array['minute'] = []
    array['weekday'] = []

    for d_time in array[field]:
      array['year'].append(d_time.year)
      array['month'].append(d_time.month)
      array['day'].append(d_time.day)
      array['hour'].append(d_time.hour)
      array['minute'].append(d_time.minute)

      array['weekday'].append(d_time.date().isoweekday())
      array['timestamp'].append(d_time.timestamp())

    return array

  def get_sensor_data(self, data):
    sd = SensorData.select() \
                   .where(SensorData.plant == data['plant']) \
                   .where(SensorData.sensor == data['sensor']) \
                   .order_by(SensorData.created_at.asc())

    return sd

  def simulated_data(self, data):
    sd = self.get_sensor_data(data)
    data_count = sd.count()

    if data_count == 0:
      other = {'plant': None, 'sensor': None}
      other['plant'] = Plant.select().where(Plant.localhost == False)[0]
      other['sensor'] = data['sensor']
      generated = []

      csd = self.get_sensor_data(other)
      data_count = csd.count()

      if data_count <= 1000:
        generated = self.predict(data, sd)
      else:
        import random
        start = random.randint(0, data_count - 1000)
        generated = self.predict(data, sd[start:start + 1000])

      for entry in sd:
        pass

      for entry in generated:
        pass

  def predict(self, data, sd):
    """ forecasting timebased sensor data
        INPUT dict
          plant - current plant object
          sensor - current sensor object

    """

    data = {}
    data['date'] = []
    data['value'] = []
    data['average'] = []

    future = {}
    future['date'] = []

    if len(sd) < 1000:
      print('not enough samples')
      return None

    for entry in sd:
      created_at = entry.created_at
      str_entry = created_at.replace('+00:00', '')
      dt_date = datetime.datetime.strptime(str_entry, '%Y-%m-%d %H:%M:%S')
      data['date'].append(dt_date)

      data['value'].append(entry.value)

    last_datetime = data['date'][-1]

    cap = int(len(data['date']) / 100 * 10)
    for i in range(0, cap):
      current = last_datetime + datetime.timedelta(minutes=30)
      future['date'].append(current)
      last_datetime = current

    data = self.datetime_to_dict(data)
    future = self.datetime_to_dict(future)

    index = pd.DatetimeIndex(data['date'])
    time_series = pd.Series(data['value'], index=index)
    rolmean = time_series.rolling(center=False, window=12).mean()

    for entry in rolmean:
      data['average'].append(entry)

    data_frame = pd.DataFrame(data)
    data_frame = data_frame[data_frame.average.notnull()]

    columns = data_frame.columns.tolist()
    columns = [c for c in columns if c not in ['value', 'average', 'date']]

    model = ExtraTreesRegressor()
    model.fit(data_frame[columns].values,
              data_frame['average'].values)

    pred_data_frame = pd.DataFrame(future)
    predictions = model.predict(pred_data_frame[columns].values)

    future['prediction'] = []
    for prediction in predictions:
      future['prediction'].append(prediction)

    if GRAPH is True:
      self.show_graph(data['date'], data['average'], future['date'], predictions)

    return future

  def insert_database(self, data):
    SensorDataPrediction.delete().where(SensorDataPrediction.plant == data['plant']) \
                                 .where(SensorDataPrediction.sensor == data['sensor']) \
                                 .execute()

    print(data)
    for key, prediction in enumerate(data['prediction']['prediction']):
      entry = SensorDataPrediction()
      entry.plant = data['plant']
      entry.sensor = data['sensor']
      entry.value = prediction
      entry.time = data['prediction']['date'][key]
      entry.save()

  def run(self, data):
    sd = self.get_sensor_data(data)
    if not sd.count() < 1000:
      data['prediction'] = self.predict(data, sd)
      self.insert_database(data)


if __name__ == '__main__':
  from models.plant import Plant
  from models.sensor import Sensor

  data = {}
  data['plant'] = Plant.get(Plant.name == 'marta')
  data['sensor'] = Sensor.get(Sensor.name == 'light')
  print(data['sensor'])
  SensorDataForecast().run(data)
  print('done')
  data['sensor'] = Sensor.get(Sensor.name == 'humidity')
  SensorDataForecast().run(data)
  print('done')
  data['sensor'] = Sensor.get(Sensor.name == 'moisture')
  SensorDataForecast().run(data)
