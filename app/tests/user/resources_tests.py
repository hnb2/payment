import json
import unittest

import mock

import auth
from tests.common.services.mocks import MockUserService

mock_user_service = MockUserService()


class ExpressTests(unittest.TestCase):
    access_token = 'my-random-user-token'

    def setUp(self):
        self.app = auth.app.test_client()

    @mock.patch(
        'auth.user.resources.UserStatusResource.user_service.get_current_profile',
        side_effect=mock_user_service.get_current_profile_none
    )
    def test_status_none(self, mock_user_service):
        rv = self.app.get('/user/status/{}'.format(self.access_token))
        self.assertEqual(rv.status_code, 200)

        json_data = json.loads(rv.data)
        self.assertEqual(json_data['subscription_status'], 'none')
        mock_user_service.assert_called_with(self.access_token)

    @mock.patch(
        'auth.user.resources.UserStatusResource.user_service.get_current_profile',
        side_effect=mock_user_service.get_current_profile_basic
    )
    def test_status_basic(self, mock_user_service):
        rv = self.app.get('/user/status/{}'.format(self.access_token))
        self.assertEqual(rv.status_code, 200)

        json_data = json.loads(rv.data)
        self.assertEqual(json_data['subscription_status'], 'basic')
        mock_user_service.assert_called_with(self.access_token)

    @mock.patch(
        'auth.user.resources.UserStatusResource.user_service.get_current_profile',
        side_effect=mock_user_service.get_current_profile_premium
    )
    def test_status_premium(self, mock_user_service):
        rv = self.app.get('/user/status/{}'.format(self.access_token))
        self.assertEqual(rv.status_code, 200)

        json_data = json.loads(rv.data)
        self.assertEqual(json_data['subscription_status'], 'premium')
        mock_user_service.assert_called_with(self.access_token)
