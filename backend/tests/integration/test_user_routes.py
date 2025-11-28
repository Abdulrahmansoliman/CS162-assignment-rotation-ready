"""Integration tests for user routes."""
import pytest
from app.services.auth.token_service import TokenService
from app.models import User, VerificationStatusEnum


@pytest.mark.integration
class TestGetCurrentUserRoute:
    """Tests for the GET /api/v1/user/me endpoint."""

    def test_get_current_user_returns_user_data(
        self,
        client,
        verified_user,
        app_context
    ):
        """Test getting current authenticated user's information."""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        response = client.get(
            '/api/v1/user/me',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['user_id'] == verified_user.user_id
        assert data['first_name'] == verified_user.first_name
        assert data['last_name'] == verified_user.last_name
        assert data['email'] == verified_user.email
        assert data['rotation_city'] is not None
        assert data['rotation_city']['city_id'] == verified_user.rotation_city_id

    def test_get_current_user_includes_rotation_city(
        self,
        client,
        verified_user,
        rotation_city,
        app_context
    ):
        """Test that rotation city data is included in response."""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        response = client.get(
            '/api/v1/user/me',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['rotation_city']['name'] == rotation_city.name
        assert data['rotation_city']['time_zone'] == rotation_city.time_zone

    def test_get_current_user_requires_auth(self, client):
        """Test that authentication is required."""
        response = client.get('/api/v1/user/me')

        assert response.status_code == 401

    def test_get_current_user_returns_404_when_user_missing(
        self,
        client,
        verified_user,
        db_session,
        app_context
    ):
        """Test that 404 is returned when user doesn't exist."""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        # Delete the user from database
        db_user = db_session.get(User, verified_user.user_id)
        db_session.delete(db_user)
        db_session.commit()

        response = client.get(
            '/api/v1/user/me',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code == 404
        data = response.get_json()
        assert data['message'] == 'User not found.'


@pytest.mark.integration
class TestGetUserByIdRoute:
    """Tests for the GET /api/v1/user/<user_id> endpoint."""

    def test_get_user_by_id_returns_user_data(
        self,
        client,
        verified_user,
        app_context
    ):
        """Test getting user by ID."""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        response = client.get(
            f'/api/v1/user/{verified_user.user_id}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['user_id'] == verified_user.user_id
        assert data['email'] == verified_user.email

    def test_get_user_by_id_requires_auth(self, client, verified_user):
        """Test that authentication is required."""
        response = client.get(f'/api/v1/user/{verified_user.user_id}')

        assert response.status_code == 401

    def test_get_user_by_id_returns_404_when_not_found(
        self,
        client,
        verified_user,
        app_context
    ):
        """Test that 404 is returned when user doesn't exist."""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        response = client.get(
            '/api/v1/user/99999',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code == 404
        data = response.get_json()
        assert data['message'] == 'User not found.'

    def test_get_user_by_id_returns_different_user_data(
        self,
        client,
        verified_user,
        db_session,
        rotation_city,
        app_context
    ):
        """Test getting a different user's data."""
        # Create another user
        other_user = User(
            first_name='Other',
            last_name='User',
            email='other@example.com',
            rotation_city_id=rotation_city.city_id,
            is_verified=True,
            status=VerificationStatusEnum.VERIFIED.code
        )
        db_session.add(other_user)
        db_session.commit()
        db_session.refresh(other_user)

        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        response = client.get(
            f'/api/v1/user/{other_user.user_id}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['user_id'] == other_user.user_id
        assert data['email'] == other_user.email


@pytest.mark.integration
class TestUpdateCurrentUserRoute:
    """Tests for the PUT /api/v1/user/me endpoint."""

    def test_update_current_user_updates_name(
        self,
        client,
        verified_user,
        db_session,
        app_context
    ):
        """Test updating user's first and last name."""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }

        response = client.put(
            '/api/v1/user/me',
            json=update_data,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['first_name'] == 'Updated'
        assert data['last_name'] == 'Name'

        # Verify in database
        db_session.expire_all()
        user = db_session.get(User, verified_user.user_id)
        assert user.first_name == 'Updated'
        assert user.last_name == 'Name'

    def test_update_current_user_updates_rotation_city(
        self,
        client,
        verified_user,
        db_session,
        app_context
    ):
        """Test updating user's rotation city."""
        # Create another rotation city
        from app.models import RotationCity
        new_city = RotationCity(
            name='Berlin',
            time_zone='Europe/Berlin',
            res_hall_location='Main Campus'
        )
        db_session.add(new_city)
        db_session.commit()
        db_session.refresh(new_city)

        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        update_data = {
            'rotation_city_id': new_city.city_id
        }

        response = client.put(
            '/api/v1/user/me',
            json=update_data,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['rotation_city']['city_id'] == new_city.city_id
        assert data['rotation_city']['name'] == 'Berlin'

    def test_update_current_user_requires_auth(self, client):
        """Test that authentication is required."""
        update_data = {'first_name': 'Updated'}

        response = client.put(
            '/api/v1/user/me',
            json=update_data
        )

        assert response.status_code == 401

    def test_update_current_user_returns_404_when_user_missing(
        self,
        client,
        verified_user,
        db_session,
        app_context
    ):
        """Test that 404 is returned when user doesn't exist."""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        # Delete the user
        db_user = db_session.get(User, verified_user.user_id)
        db_session.delete(db_user)
        db_session.commit()

        update_data = {'first_name': 'Updated'}

        response = client.put(
            '/api/v1/user/me',
            json=update_data,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code == 404
        data = response.get_json()
        assert data['message'] == 'User not found.'

    def test_update_current_user_invalid_city_id(
        self,
        client,
        verified_user,
        app_context
    ):
        """Test that invalid city ID returns error."""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        update_data = {
            'rotation_city_id': 99999  # Non-existent city
        }

        response = client.put(
            '/api/v1/user/me',
            json=update_data,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data or 'message' in data

    def test_update_current_user_null_city_id(
        self,
        client,
        verified_user,
        app_context
    ):
        """Test that null city ID returns error."""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        update_data = {
            'rotation_city_id': None
        }

        response = client.put(
            '/api/v1/user/me',
            json=update_data,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code == 500

    def test_update_current_user_invalid_city_id_type(
        self,
        client,
        verified_user,
        app_context
    ):
        """Test that invalid city ID type returns error."""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        update_data = {
            'rotation_city_id': 'not_a_number'
        }

        response = client.put(
            '/api/v1/user/me',
            json=update_data,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code == 500

    def test_update_current_user_partial_update(
        self,
        client,
        verified_user,
        db_session,
        app_context
    ):
        """Test that only specified fields are updated."""
        original_email = verified_user.email
        original_last_name = verified_user.last_name

        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        update_data = {
            'first_name': 'NewFirst'
        }

        response = client.put(
            '/api/v1/user/me',
            json=update_data,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['first_name'] == 'NewFirst'
        assert data['email'] == original_email

        # Verify in database
        db_session.expire_all()
        user = db_session.get(User, verified_user.user_id)
        assert user.first_name == 'NewFirst'
        assert user.last_name == original_last_name

    def test_update_current_user_ignores_non_allowed_fields(
        self,
        client,
        verified_user,
        db_session,
        app_context
    ):
        """Test that non-allowed fields are not updated."""
        original_email = verified_user.email

        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        update_data = {
            'first_name': 'Updated',
            'email': 'newemail@example.com',  # Not allowed
            'is_verified': False  # Not allowed
        }

        response = client.put(
            '/api/v1/user/me',
            json=update_data,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['first_name'] == 'Updated'
        assert data['email'] == original_email  # Should remain unchanged

        # Verify in database
        db_session.expire_all()
        user = db_session.get(User, verified_user.user_id)
        assert user.email == original_email
        assert user.is_verified == True

    def test_update_current_user_all_fields(
        self,
        client,
        verified_user,
        db_session,
        app_context
    ):
        """Test updating multiple allowed fields at once."""
        from app.models import RotationCity
        new_city = RotationCity(
            name='Tokyo',
            time_zone='Asia/Tokyo',
            res_hall_location='Central Dorm'
        )
        db_session.add(new_city)
        db_session.commit()
        db_session.refresh(new_city)

        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        update_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'rotation_city_id': new_city.city_id
        }

        response = client.put(
            '/api/v1/user/me',
            json=update_data,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['first_name'] == 'Jane'
        assert data['last_name'] == 'Doe'
        assert data['rotation_city']['city_id'] == new_city.city_id


@pytest.mark.integration
class TestUserResponseSchema:
    """Tests for user response schema and serialization."""

    def test_user_response_includes_all_required_fields(
        self,
        client,
        verified_user,
        app_context
    ):
        """Test that response includes all required fields."""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        response = client.get(
            '/api/v1/user/me',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        data = response.get_json()
        required_fields = ['user_id', 'first_name', 'last_name', 'email', 'rotation_city']
        for field in required_fields:
            assert field in data

    def test_user_response_rotation_city_structure(
        self,
        client,
        verified_user,
        rotation_city,
        app_context
    ):
        """Test that rotation city has correct structure."""
        tokens = TokenService.generate_tokens(verified_user)
        access_token = tokens['access_token']

        response = client.get(
            '/api/v1/user/me',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        data = response.get_json()
        city = data['rotation_city']
        required_city_fields = ['city_id', 'name', 'time_zone', 'res_hall_location']
        for field in required_city_fields:
            assert field in city
