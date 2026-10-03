from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Cat


class CatApiTests(APITestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user('owner', password='testpass123')
        self.other = get_user_model().objects.create_user('other', password='testpass123')
        self.cat = Cat.objects.create(name='Murka', color='White', birth_year=2020, owner=self.owner)

    def test_partial_update_and_owner_permission(self):
        url = f'/cats/{self.cat.id}/'
        self.client.force_authenticate(self.other)
        self.assertEqual(self.client.patch(url, {'name': 'Changed'}).status_code, 403)
        self.client.force_authenticate(self.owner)
        response = self.client.patch(url, {'achievements': [{'achievement_name': 'Playful'}]}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(self.cat.achievements.values_list('name', flat=True)), ['Playful'])

    def test_duplicate_name_for_same_owner_returns_validation_error(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post('/cats/', {
            'name': 'Murka', 'color': 'White', 'birth_year': 2020
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Cat.objects.count(), 1)
