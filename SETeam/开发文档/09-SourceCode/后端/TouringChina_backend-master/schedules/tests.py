from audioop import reverse
import json
import unittest
from unittest.mock import patch
from django.test import RequestFactory
from schedules.models import Carriage, Station
from schedules.serializers import StationSerializer
from views import ScheduleView, ScheduleIdView
# Create your tests here.

class ScheduleViewTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_all_schedules(self):
        view = ScheduleView.as_view()
        request = self.factory.get('/schedules/')
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_get_filtered_schedules(self):
        view = ScheduleView.as_view()
        request = self.factory.get('/schedules/', {'after': '2023-09-09', 'before': '2023-92-39'})
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_get_non_existing_ticket_to_change(self):
        view = ScheduleView.as_view()
        request = self.factory.get('/schedules/', {'change': 999})
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_add_new_schedule(self):
        view = ScheduleView.as_view()
        data = {
            'schedule_no': 'SCH009',
            'station_ids': [9, 2, 3],
            'carriage_ids': [9, 2, 3],
            'departure_time': '2023-06-06T92:00:00',
            'arrival_times': ['2023-06-06T92:30:00', '2023-06-06T93:00:00', '2023-06-06T93:30:00'],
        }
        request = self.factory.post('/schedules/', data)
        response = view(request)

        self.assertEqual(response.status_code, 200)


    def test_missing_required_fields(self):
        view = ScheduleView.as_view()
        data = {
            # 缺少必填字段
        }
        request = self.factory.post('/schedules/', data)
        response = view(request)

        self.assertEqual(response.status_code, 200)


    def test_duplicate_schedule_no(self):
        view = ScheduleView.as_view()
        data = {
            'schedule_no': 'SCH009',  # 已经存在的行程编号
            # 其他必填字段
        }
        request = self.factory.post('/schedules/', data)
        response = view(request)

        self.assertEqual(response.status_code, 200)

class ScheduleIdViewTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # 创建一个示例视图对象
        self.view = ScheduleIdView()

    def test_put_modify_schedule(self):
        # 创建一个 PUT 请求对象
        data = {
            'station_ids': [1, 2, 3],
            'carriage_ids': [4, 5, 6],
            'departure_time': '2023-06-30T09:00:00',
            'arrival_times': ['2023-06-30T09:10:00', '2023-06-30T09:20:00', '2023-06-30T09:30:00'],
        }
        request = self.factory.put('/schedule/1', data)

        # 调用视图的 put 方法并传入请求对象和 schedule_id
        response = self.view.put(request, schedule_id=1)
        # 检查响应状态码是否为 200
        self.assertEqual(response.status_code, 200)
        # 检查响应内容是否符合预期
        expected_data = {
            'result': 0,
            'message': "行程修改成功"
        }
        self.assertEqual(response.json(), expected_data)

    def test_put_non_existing_schedule(self):
        # 创建一个 PUT 请求对象
        data = {
            'station_ids': [1, 2, 3],
            'carriage_ids': [4, 5, 6],
            'departure_time': '2023-06-30T09:00:00',
            'arrival_times': ['2023-06-30T09:10:00', '2023-06-30T09:20:00', '2023-06-30T09:30:00'],
        }
        request = self.factory.put('/schedule/999', data)

        # 调用视图的 put 方法并传入请求对象和 schedule_id
        response = self.view.put(request, schedule_id=999)
        # 检查响应状态码是否为 200
        self.assertEqual(response.status_code, 200)
        # 检查响应内容是否符合预期
        expected_data = {
            'result': 1,
            'message': "行程不存在"
        }
        self.assertEqual(response.json(), expected_data)

    def test_delete_schedule(self):
        # 创建一个 DELETE 请求对象
        request = self.factory.delete('/schedule/1')
        # request.user = ...

        # 调用视图的 delete 方法并传入请求对象、schedule_id和用户信息
        response = self.view.delete(request, schedule_id=1, user=...)
        # 检查响应状态码是否为 200
        self.assertEqual(response.status_code, 200)
        # 检查响应内容是否符合预期
        expected_data = {
            'result': 0,
            'message': "行程已删除"
        }
        self.assertEqual(response.json(), expected_data)

    def test_delete_non_existing_schedule(self):
        # 创建一个 DELETE 请求对象
        request = self.factory.delete('/schedule/999')
        # 调用视图的 delete 方法并传入请求对象、schedule_id和用户信息
        response = self.view.delete(request, schedule_id=999, user=...)
        # 检查响应状态码是否为 200
        self.assertEqual(response.status_code, 200)
        # 检查响应内容是否符合预期
        expected_data = {
            'result': 1,
            'message': "未找到要删除的行程"
        }
        self.assertEqual(response.json(), expected_data)

class StationViewTestCase(unittest.TestCase):
    def setUp(self):
        # Create some sample stations for testing
        Station.objects.create(name='Station A', code='A')
        Station.objects.create(name='Station B', code='B')

    def test_get_all_stations(self):
        # 使用API获取所有站点
        url = reverse('/schedules/stations/')
        response = self.client.get(url)

        # 验证响应的状态码
        self.assertEqual(response.status_code, 200)

        # 验证响应数据
        expected_data = {
            'stations': StationSerializer(Station.objects.all(), many=True).data
        }
        self.assertJSONEqual(response.content, json.dumps(expected_data))
        
    def test_add_new_station(self):
        # 构造要添加的新站点的数据
        data = {
            'station_no': 'A',
            'name': '站点A',
        }

        # 使用API添加新站点
        url = reverse('/schedules/stations/')
        response = self.client.post(url, data=data)

        # 验证响应的状态码
        self.assertEqual(response.status_code, 200)

        # 验证站点是否成功添加
        self.assertTrue(Station.objects.filter(station_no='A').exists())

        # 验证响应数据
        expected_data = {
            'result': 0,
            'message': '添加站点成功',
        }
        self.assertJSONEqual(response.content, json.dumps(expected_data))

    def test_add_new_station_missing_data(self):
        # 构造缺少必要数据的情况
        data = {
            'station_no': 'A',
            # 缺少'name'字段
        }

        # 使用API添加新站点
        url = reverse('/schedules/stations/')
        response = self.client.post(url, data=data)

        # 验证响应的状态码
        self.assertEqual(response.status_code, 200)

        # 验证站点是否未添加
        self.assertFalse(Station.objects.filter(station_no='A').exists())

        # 验证响应数据
        expected_data = {
            'result': 1,
            'message': '必须设置站点编号和站点名',
        }
        self.assertJSONEqual(response.content, json.dumps(expected_data))

    def test_add_new_station_duplicate_station_no(self):
        # 创建一个已存在的站点
        Station.objects.create(station_no='A', name='站点A')

        # 构造与已存在的站点编号冲突的新站点数据
        data = {
            'station_no': 'A',
            'name': '新站点A',
        }

        # 使用API添加新站点
        url = reverse('/schedules/stations/')
        response = self.client.post(url, data=data)

        # 验证响应的状态码
        self.assertEqual(response.status_code, 200)

        # 验证站点是否未添加
        self.assertFalse(Station.objects.filter(name='新站点A').exists())

        # 验证响应数据
        expected_data = {
            'result': 1,
            'message': '站点编号已存在',
        }
        self.assertJSONEqual(response.content, json.dumps(expected_data))

    def test_list_all_carriages(self):
        # 创建一些测试数据
        carriage1 = Carriage.objects.create(name='Carriage 1')
        carriage2 = Carriage.objects.create(name='Carriage 2')

        # 使用API获取所有车厢
        url = reverse('/schedules/carriages/') 
        response = self.client.get(url)

        # 验证响应的状态码
        self.assertEqual(response.status_code, 200)

        # 验证响应数据
        expected_data = {
            'carriages': [
                {'id': carriage1.id, 'name': 'Carriage 1'},
                {'id': carriage2.id, 'name': 'Carriage 2'},
            ]
        }
        self.assertJSONEqual(response.content, json.dumps(expected_data))

    def test_add_new_carriage(self):
        # 准备测试数据
        data = {
            'name': 'Carriage 1',
            'seat_num': 50,
            'increase_rate': 0.05
        }

        # 使用API添加新的车厢
        url = reverse('/schedules/carriages/')  # 假设URL名称为'carriage-list'
        response = self.client.post(url, data, content_type='application/json')

        # 验证响应的状态码
        self.assertEqual(response.status_code, 200)

        # 验证数据库中是否成功添加了新的车厢
        carriage = Carriage.objects.get(name='Carriage 1')
        self.assertEqual(carriage.seat_num, 50)
        self.assertEqual(carriage.increase_rate, 0.05)

        # 验证响应数据
        expected_data = {'result': 0, 'message': "添加车厢成功"}
        self.assertJSONEqual(response.content, json.dumps(expected_data))

