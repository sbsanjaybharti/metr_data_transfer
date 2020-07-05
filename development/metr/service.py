import collections

from .serializers import DeviceSerializer
from .models import Device, Dimension, DeviceDimension


class DataProcess:
    def __init__(self, values):
        # self.data = data
        self.slice_data = collections.defaultdict(list)
        self.latest_data = None
        self.due_date_data = None
        self.dimention = {}
        self.__get_dimension()
        self.device = self.get_device(values['device'])
        self.__process(values['data'])

    def __process(self, values):
        date_time = {}
        due_date = {}
        temp = []
        for data in values:
            if self.dimention[data['dimension']] == 1:
                date_time[data['storagenr']] = data['value']
                continue
            if self.dimention[data['dimension']] == 2:
                due_date[data['storagenr']] = data['value']
                continue
            data.update({'device': self.device.id})
            data.update({'dimension': self.dimention[data['dimension']]})
            temp.append(data)

        for item in temp:
            if item.get('storagenr') in date_time.keys():
                item.update({'date': date_time[item.get('storagenr')]})
                item.update({'type': 'reading'})
                self.slice_data[item['dimension']].append(item)
                continue
            if item.get('storagenr') in due_date.keys():
                item.update({'date': due_date[item.get('storagenr')]})
                item.update({'type': 'due'})
                self.slice_data[item['dimension']].append(item)
                continue
            last_storagenr = max(max(date_time.keys()), max(due_date.keys()))

            item.update({'date': due_date[last_storagenr]})
            if last_storagenr in date_time.keys():
                item.update({'type': 'reading'})
            else:
                item.update({'type': 'due'})

            self.slice_data[item['dimension']].append(item)

        return self.get()

    def get(self):
        return self.slice_data

    def get_latest_data(self):
        return self.latest_data

    def get_due_date_data(self):
        return self.due_date_data

    def get_device(self, data):
        device = Device.objects.filter(identnr=data['identnr']).first()
        if device is None:
            device = DeviceSerializer(data=data)
            if device.is_valid():
                device.save()
                return Device.objects.filter(identnr=data['identnr']).first()

        return device

    def __get_dimension(self):
        for row in Dimension.objects.all():
            self.dimention[row.name] = row.id

class CsvGenerate:
    def __init__(self):
        pass

    def get(self):
        data = DeviceDimension.objects.all()