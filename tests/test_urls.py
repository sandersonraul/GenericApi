from tests import test_base
from users.models import User

class TestUsersUrls(test_base.TestBase):

  def test_register(self):
    data = {
      "username": "test",
      "email": "raul.oliveira26@gmail.com",   
      "password":"admin"
    }
    response = self.client.post('/api/register', data)
    assert response.status_code == 200
  
  def test_login_no_user(self):
    data = {
      "email": "test",
      "password":"admin"
    }
    response = self.client.post('/api/login', data)
    assert response.data == {'detail': 'User not found!'}

  def test_login_no_data(self):
    response = self.client.post('/api/login')
    assert response.data == {'detail': 'email and password are required'}

  def test_login_wrong_password(self):
    user = User.objects.create(username='test', email='test@test.com', is_active=True)
    user.set_password('test')
    user.save()
    data = {
      "email": "test@test.com",
      "password":"admin1"
    } 
    response = self.client.post('/api/login', data)
    assert response.data == {'detail': 'Incorrect password!'} 

  def test_login(self):
    user = User.objects.create(username='test', email='test@test.com', is_active=True)
    user.set_password('test')
    user.save()
    data = {
      "email": "test@test.com",
      "password":"test"
    } 
    response = self.client.post('/api/login', data)
    assert response.status_code == 200

  def test_view(self):
    self.create_user()
    self.login()
    response = self.client.get('/api/user/test@test.com')
    assert response.status_code == 200
