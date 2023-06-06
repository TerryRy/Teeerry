from audioop import reverse
import datetime
from pstats import Stats, StatsProfile
import statistics
from telnetlib import STATUS
from django.test import TestCase
from psutil import _Status
from rest_framework.test import APIRequestFactory, APITestCase
from scipy import stats
from accounts.models import Account
from contacts.models import Contact
from schedules.models import Carriage, Schedule, ScheduleToCarriage, Station
from views import TicketView
from models import User, Ticket

# Create your tests here.
class TicketViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = TicketView.as_view()

    def test_get_tickets(self):
        # 创建用户和票务数据
        user = User.objects.create(username='testuser')
        ticket1 = Ticket.objects.create(user=user, name='Ticket 1')
        ticket2 = Ticket.objects.create(user=user, name='Ticket 2')

        # 创建 GET 请求对象
        request = self.factory.get('/tickets/')
        request.user = user

        # 调用视图函数
        response = self.view(request, user=user)

        # 断言响应状态码和数据
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['tickets']), 2)

    def test_buy_ticket(self):
        # 创建用户和其他必要的数据
        user = User.objects.create(username='testuser')
        contact = Contact.objects.create(user=user, name='Test Contact')
        schedule = Schedule.objects.create(name='Test Schedule')
        carriage = Carriage.objects.create(name='Test Carriage')
        ori_station = Station.objects.create(name='Origin Station')
        dst_station = Station.objects.create(name='Destination Station')
        schedule2carriage = ScheduleToCarriage.objects.create(schedule=schedule, carriage=carriage)

        # 创建 POST 请求对象
        data = {
            'schedule_id': schedule.id,
            'contact_id': contact.id,
            'carriage_id': carriage.id,
            'ori_station_id': ori_station.id,
            'dst_station_id': dst_station.id,
        }
        request = self.factory.post('/schedules/tickets/', data=data)
        request.user = user

        # 调用视图函数
        response = self.view(request, user=user)

        # 断言响应状态码和数据
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['result'], 0)
        self.assertEqual(response.data['message'], "订票成功，请支付订单")

class TicketIdViewTest(APITestCase):
    def setUp(self):
        # Create a test user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Create a test ticket
        self.ticket = Ticket.objects.create(amount=100, seat_no=1, user=self.user)

    def test_get_ticket(self):
        # Send GET request to retrieve the ticket
        url = reverse('schedules\tickets\id', args=[self.ticket.id])
        response = self.client.get(url)

        # Verify the response
        self.assertEqual(response.status_code, statistics.HTTP_200_OK)
        self.assertEqual(response.data['result'], 0)
        self.assertEqual(response.data['message'], "Success")
        self.assertEqual(response.data['ticket']['id'], self.ticket.id)
        # Add more assertions to verify other fields of the ticket

    def test_get_nonexistent_ticket(self):
        # Send GET request with a non-existent ticket ID
        url = reverse('schedules\tickets\id', args=[9999])
        response = self.client.get(url)

        # Verify the response
        self.assertEqual(response.status_code, Stats.HTTP_200_OK)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "车票未找到")

    def test_get_ticket_unauthorized(self):
        # Create a new ticket with a different user
        another_user = User.objects.create_user(username='anotheruser', password='testpassword')
        ticket = Ticket.objects.create(amount=200, seat_no=2, user=another_user)

        # Send GET request to retrieve the ticket using unauthorized user
        url = reverse('schedules\tickets\id', args=[ticket.id])
        response = self.client.get(url)

        # Verify the response
        self.assertEqual(response.status_code, StatsProfile.HTTP_200_OK)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "车票未找到")

    def test_change_ticket(self):
        # Prepare request data for ticket change
        new_schedule_id = 2
        carriage_id = 3
        data = {
            'new_schedule_id': new_schedule_id,
            'carriage_id': carriage_id,
        }

        # Send PUT request to change the ticket
        url = reverse('/schedules/tickets/<id>', args=[self.ticket.id])
        response = self.client.put(url, data=data)

        # Verify the response
        self.assertEqual(response.status_code, _Status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 0)
        self.assertEqual(response.data['message'], "车票已改签")
        # Add more assertions to verify the updated ticket details

    def test_change_ticket_invalid_data(self):
        # Send PUT request with invalid request data
        data = {}

        url = reverse('/schedules/tickets/<id>', args=[self.ticket.id])
        response = self.client.put(url, data=data)

        # Verify the response
        self.assertEqual(response.status_code, _Status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "改签必须指定目标车票和座位号")

    def test_change_nonexistent_ticket(self):
        # Send PUT request with a non-existent ticket ID
        new_schedule_id = 2
        carriage_id = 3
        data = {
            'new_schedule_id': new_schedule_id,
            'carriage_id': carriage_id,
        }

        url = reverse('/schedules/tickets/<id>', args=[9999])
        response = self.client.put(url, data=data)

        # Verify the response
        self.assertEqual(response.status_code, _Status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "车票未找到")

    def test_change_ticket_unauthorized(self):
        # Create a new ticket with a different user
        another_user = User.objects.create_user(username='anotheruser', password='testpassword')
        ticket = Ticket.objects.create(amount=200, seat_no=2, user=another_user)

        # Prepare request data for ticket change
        new_schedule_id = 2
        carriage_id = 3
        data = {
            'new_schedule_id': new_schedule_id,
            'carriage_id': carriage_id,
        }

        # Send PUT request to change the ticket using unauthorized user
        url = reverse('/schedules/tickets/<id>', args=[ticket.id])
        response = self.client.put(url, data=data)

        # Verify the response
        self.assertEqual(response.status_code, _Status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "车票未找到")

    def test_pay_for_ticket(self):
        # Create a test account for payment
        account = Account.objects.create(user=self.user, amount=200)

        # Prepare request data for ticket payment
        account_id = account.id
        data = {
            'account_id': account_id,
        }

        # Send PATCH request to pay for the ticket
        url = reverse('/schedules/tickets/<id>', args=[self.ticket.id])
        response = self.client.patch(url, data=data)

        # Verify the response
        self.assertEqual(response.status_code, STATUS.HTTP_200_OK)
        self.assertEqual(response.data['result'], 0)
        self.assertEqual(response.data['message'], "车票订单支付成功")
        # Add more assertions to verify the updated ticket and account details

    def test_pay_for_ticket_invalid_data(self):
        # Send PATCH request with invalid request data
        data = {}

        url = reverse('/schedules/tickets/<id>', args=[self.ticket.id])
        response = self.client.patch(url, data=data)

        # Verify the response
        self.assertEqual(response.status_code, STATUS.HTTP_200_OK)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "必须选择支付账户")

    def test_pay_for_nonexistent_ticket(self):
        # Send PATCH request with a non-existent ticket ID
        account_id = 1
        data = {
            'account_id': account_id,
        }

        url = reverse('/schedules/tickets/<id>', args=[9999])
        response = self.client.patch(url, data=data)

        # Verify the response
        self.assertEqual(response.status_code, STATUS.HTTP_200_OK)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "未找到要支付的车票")

    def test_pay_for_paid_ticket(self):
        # Mark the ticket as already paid
        self.ticket.is_paid = True
        self.ticket.save()

        # Create a test account for payment
        account = Account.objects.create(user=self.user, amount=200)

        # Prepare request data for ticket payment
        account_id = account.id
        data = {
            'account_id': account_id,
        }

        # Send PATCH request to pay for the ticket
        url = reverse('/schedules/tickets/<id>', args=[self.ticket.id])
        response = self.client.patch(url, data=data)

        # Verify the response
        self.assertEqual(response.status_code, STATUS.HTTP_200_OK)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "车票已支付")

    def test_pay_for_modified_ticket(self):
        # Mark the ticket as having modified schedule
        self.ticket.is_schedule_modified = True
        self.ticket.save()

        # Create a test account for payment
        account = Account.objects.create(user=self.user, amount=200)

        # Prepare request data for ticket payment
        account_id = account.id
        data = {
            'account_id': account_id,
        }

        # Send PATCH request to pay for the ticket
        url = reverse('/schedules/tickets/<id>', args=[self.ticket.id])
        response = self.client.patch(url, data=data)

        # Verify the response
        self.assertEqual(response.status_code, STATUS.HTTP_200)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "所购列车行程已更改，请重新购票")

    def test_pay_for_expired_ticket(self):
        # Expire the ticket
        self.ticket.create_time = datetime.now() - datetime.timedelta(days=2)
        self.ticket.save()

        # Create a test account for payment
        account = Account.objects.create(user=self.user, amount=200)

        # Prepare request data for ticket payment
        account_id = account.id
        data = {
            'account_id': account_id,
        }

        # Send PATCH request to pay for the ticket
        url = reverse('/schedules/tickets/<id>', args=[self.ticket.id])
        response = self.client.patch(url, data=data)

        # Verify the response
        self.assertEqual(response.status_code, STATUS.HTTP_200_OK)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "车票订单已过期，请删除订单")

    def test_pay_with_insufficient_balance(self):
        # Create a test account with insufficient balance for payment
        account = Account.objects.create(user=self.user, amount=50)

        # Prepare request data for ticket payment
        account_id = account.id
        data = {
            'account_id': account_id,
        }

        # Send PATCH request to pay for the ticket
        url = reverse('/schedules/tickets/<id>', args=[self.ticket.id])
        response = self.client.patch(url, data=data)

        # Verify the response
        self.assertEqual(response.status_code, STATUS.HTTP_200_OK)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "账户余额不足")

    def test_delete_unpaid_ticket_order(self):
        # Send DELETE request to delete an unpaid ticket order
        url = reverse('/schedules/tickets/<id>', args=[self.ticket.id])
        response = self.client.delete(url)

        # Verify the response
        self.assertEqual(response.status_code, STATUS.HTTP_200_OK)
        self.assertEqual(response.data['result'], 0)
        self.assertEqual(response.data['message'], "订单已删除")
        # Add more assertions to verify that the ticket is deleted

    def test_delete_paid_ticket(self):
        # Mark the ticket as paid
        self.ticket.is_paid = True
        self.ticket.save()

        # Send DELETE request to cancel a paid ticket
        account = Account.objects.create(user=self.user, amount=200)
        account_id = account.id
        data = {
            'account_id': account_id,
        }

        url = reverse('/schedules/tickets/<id>', args=[self.ticket.id])
        response = self.client.delete(url, data=data)

        # Verify the response
        self.assertEqual(response.status_code, STATUS.HTTP_200_OK)
        self.assertEqual(response.data['result'], 0)
        self.assertEqual(response.data['message'], "订单已取消")
        # Add more assertions to verify the refunded amount and updated account details

    def test_delete_paid_ticket_no_account_selected(self):
        # Mark the ticket as paid
        self.ticket.is_paid = True
        self.ticket.save()

        # Send DELETE request to cancel a paid ticket without selecting an account
        data = {}

        url = reverse('/schedules/tickets/<id>', args=[self.ticket.id])
        response = self.client.delete(url, data=data)

        # Verify the response
        self.assertEqual(response.status_code, STATUS.HTTP_200_OK)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "取消车票必须选择退款账户")

    def test_delete_nonexistent_ticket(self):
        # Send DELETE request with a non-existent ticket ID
        account_id = 1
        data = {
            'account_id': account_id,
        }

        url = reverse('/schedules/tickets/<id>', args=[9999])
        response = self.client.delete(url, data=data)

        # Verify the response
        self.assertEqual(response.status_code, STATUS.HTTP_200_OK)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "订单未找到")

    def test_delete_unmodifiable_ticket(self):
        # Mark the ticket as unmodifiable
        self.ticket.is_schedule_modified = True
        self.ticket.save()

        # Send DELETE request to delete an unmodifiable ticket
        url = reverse('/schedules/tickets/<id>', args=[self.ticket.id])
        response = self.client.delete(url)

        # Verify the response
        self.assertEqual(response.status_code, STATUS.HTTP_200_OK)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "订单不可删除")

    def test_delete_uncancelable_ticket(self):
        # Mark the ticket as uncancelable
        self.ticket.is_schedule_modified = False
        self.ticket.is_paid = False
        self.ticket.save()

        # Send DELETE request to delete an uncancelable ticket
        url = reverse('/schedules/tickets/<id>', args=[self.ticket.id])
        response = self.client.delete(url)

        # Verify the response
        self.assertEqual(response.status_code, STATUS.HTTP_200_OK)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "订单不可取消")

    def test_delete_expired_ticket(self):
        # Expire the ticket
        self.ticket.create_time = datetime.now() - datetime.timedelta(days=2)
        self.ticket.save()

        # Send DELETE request to delete an expired ticket
        url = reverse('/schedules/tickets/<id>', args=[self.ticket.id])
        response = self.client.delete(url)

        # Verify the response
        self.assertEqual(response.status_code, STATUS.HTTP_200_OK)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "订单已过期，请删除订单")