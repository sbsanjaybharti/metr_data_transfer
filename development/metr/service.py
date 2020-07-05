#!/usr/bin/env python3
"""
Import packages
"""
import collections
from .serializers import DeviceSerializer, DeviceDimensionSerializer, MeasurementSerializer, DueSerializer
from .models import Device, Dimension, DeviceDimension


# Converting gateway raw data into ORM data
class DataProcess:
    """
    request raw data
    response data in form of different method
    """
    def __init__(self, values):
        """
        request data views in raw data
        :param values:
        """
        self.slice_data = collections.defaultdict(list)
        self.latest_data = None
        self.due_date_data = None
        self.dimention = {}
        self.__get_dimension()
        self.device = self.get_device(values['device'])
        self.__process(values['data'])

    def __process(self, values):
        """
        internal method used to process data
        request data:
        {
            "data":[
                { // Date and time of the measurement
                    "value":"2020-06-26T06:49:00.000000",
                    "tariff":0,
                    "subunit":0,
                    "dimension":"Time Point (time & date)",
                    "storagenr":0
                },
                { // Latest value from the device
                    "value":29690,
                    "tariff":0,
                    "subunit":0,
                    "dimension":"Energy (kWh)",
                    "storagenr":0
                },
                { // The due date
                    "value":"2019-09-30T00:00:00.000000",
                    "tariff":0,
                    "subunit":0,
                    "dimension":"Time Point (date)",
                    "storagenr":1
                },
                { // The value at the due date
                    "value":16274,
                    "tariff":0,
                    "subunit":0,
                    "dimension":"Energy (kWh)",
                    "storagenr":1
                }
            ],
            "device":{
                "type":4, //Device type
                "status":0,
                "identnr":83251076, //Device ID
                "version":0, //Device version
                "accessnr":156,
                "manufacturer":5317 //Device manufacturer
                }
        }
        :param values:
        :return:
        {
            "data":[
                { // Latest value from the device
                    "value":29690,
                    "tariff":0,
                    "subunit":0,
                    "dimension":"Energy (kWh)",
                    "storagenr":0
                    "date":"2020-06-26T06:49:00.000000",
                    "type": reading
                },
                { // The value at the due date
                    "value":16274,
                    "tariff":0,
                    "subunit":0,
                    "dimension":"Energy (kWh)",
                    "storagenr":1
                    "date":"2019-09-30T00:00:00.000000",
                    "type": due
                }
            ],
            "device":{
                "type":4, //Device type
                "status":0,
                "identnr":83251076, //Device ID
                "version":0, //Device version
                "accessnr":156,
                "manufacturer":5317 //Device manufacturer
                }
        }

        """
        date_time = {}  # Variable to store reading data and time after slicing
        due_date = {}  # Variable to store due data after slicing
        temp = []   # Variable to store json after slicing

        # Iteration used to get all
        # date and time  falling in iteration
        # Used to clean the data
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

        # Merging reading date time and due date with slice data
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
        """
        Return slice data stored in class variable
        :return:
        """
        return self.slice_data

    def get_latest_data(self):
        """
        return reading data and time stored in class variable
        :return:
        """
        return self.latest_data

    def get_due_date_data(self):
        """
        return date data stored in class variable
        :return:
        """
        return self.due_date_data

    def get_device(self, data):
        """
        if device exist:
            return device detail
        else:
            create new device
            and return new created device
        :param data:
        :return:
        """
        device = Device.objects.filter(identnr=data['identnr']).first()
        if device is None:
            device = DeviceSerializer(data=data)
            if device.is_valid():
                device.save()
                return Device.objects.filter(identnr=data['identnr']).first()

        return device

    def __get_dimension(self):
        """
        create dist of dimension and store in dimension class variable
        :return:
        """
        for row in Dimension.objects.all():
            self.dimention[row.name] = row.id


class MessageProcess:
    """
    Proxy pattern
    Class function as a interface to resource(DataProcess)
    """
    def __init__(self, request):
        """ request data send to other resource to process """
        self.data = DataProcess(request)

    def set(self):
        """ Process data is stored in database """
        data = self.data

        # Iteration used store each record
        for row in dict(data.get()):

            item = {
                'device': data.device.id,
                'dimension': row
            }
            # if dimension of a specific device exist then fetch the data for process
            dd = DeviceDimension.objects.filter(device=data.device.id, dimension=row).first()
            if dd:
                # if exist then retrieve the data
                dd = DeviceDimensionSerializer(dd)
            else:
                # if not then create new one
                dd = DeviceDimensionSerializer(data=item)
                if dd.is_valid() is False:
                    return False
                dd.save()
            # Internal iteration for storing measurement or due date data
            for item in data.slice_data[row]:
                item.update({'device_dimension': dd.data.get('id')})
                if item['type'] == 'reading':
                    # store in measurement table if its a reading info
                    mesurement = MeasurementSerializer(data=item)
                    if mesurement.is_valid() is False:
                        return False
                    mesurement.save()
                else:
                    # store in due table if its a due date info
                    due = DueSerializer(data=item)
                    if due.is_valid() is False:
                        return False
                    due.save()
        return True
