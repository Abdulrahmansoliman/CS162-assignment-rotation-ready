"""
Integration tests for rotation city routes
"""
import pytest
from app.models.rotation_city import RotationCity


class TestRotationCityRoutes:
    """Test suite for /api/v1/rotation-city endpoints"""

    def test_get_all_rotation_cities_success(self, client, rotation_city):
        """Test GET /api/v1/rotation-city/ returns all cities"""
        response = client.get('/api/v1/rotation-city/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Verify response structure
        city = data[0]
        assert 'city_id' in city
        assert 'name' in city
        assert 'time_zone' in city

    def test_get_all_rotation_cities_empty(self, client):
        """Test GET /api/v1/rotation-city/ with no cities"""
        response = client.get('/api/v1/rotation-city/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_rotation_city_by_id_success(self, client, rotation_city):
        """Test GET /api/v1/rotation-city/<id> returns specific city"""
        response = client.get(
            f'/api/v1/rotation-city/{rotation_city.city_id}'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['city_id'] == rotation_city.city_id
        assert data['name'] == rotation_city.name
        assert data['time_zone'] == rotation_city.time_zone
        assert 'res_hall_location' in data

    def test_get_rotation_city_by_id_not_found(self, client):
        """Test GET /api/v1/rotation-city/<id> with non-existent ID"""
        response = client.get('/api/v1/rotation-city/99999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Rotation city not found'

    def test_get_rotation_city_multiple_cities(self, client, db_session):
        """Test GET /api/v1/rotation-city/ returns multiple cities"""
        # Create multiple cities
        city1 = RotationCity(
            name="San Francisco",
            time_zone="America/Los_Angeles",
            res_hall_location="123 Market St"
        )
        city2 = RotationCity(
            name="Berlin",
            time_zone="Europe/Berlin",
            res_hall_location="456 Brandenburg St"
        )
        city3 = RotationCity(
            name="Seoul",
            time_zone="Asia/Seoul"
        )
        
        db_session.add(city1)
        db_session.add(city2)
        db_session.add(city3)
        db_session.commit()
        
        response = client.get('/api/v1/rotation-city/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3
        
        city_names = [city['name'] for city in data]
        assert "San Francisco" in city_names
        assert "Berlin" in city_names
        assert "Seoul" in city_names
