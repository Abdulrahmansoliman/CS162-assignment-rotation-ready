"""
Integration tests for value routes
"""


class TestValueRoutes:
    """Test suite for /api/v1/value endpoints"""

    def test_get_all_values_success(self, client, boolean_value, text_value):
        """Test GET /api/v1/value/ returns all values"""
        response = client.get('/api/v1/value/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 2
        
        # Verify response structure
        value = data[0]
        assert 'value_id' in value
        assert 'tag_id' in value

    def test_get_all_values_empty(self, client):
        """Test GET /api/v1/value/ with no values"""
        response = client.get('/api/v1/value/')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'No values found'

    def test_get_value_by_id_success(self, client, boolean_value):
        """Test GET /api/v1/value/<id> returns specific value"""
        response = client.get(f'/api/v1/value/{boolean_value.value_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['value_id'] == boolean_value.value_id
        assert data['tag_id'] == boolean_value.tag_id
        assert data['boolean_val'] == boolean_value.boolean_val

    def test_get_value_by_id_not_found(self, client):
        """Test GET /api/v1/value/<id> with non-existent ID"""
        response = client.get('/api/v1/value/99999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Value not found'

    def test_create_boolean_value_success(
        self, client, auth_headers, boolean_tag
    ):
        """Test POST /api/v1/value/ creates boolean value"""
        value_data = {
            'tag_id': boolean_tag.tag_id,
            'boolean_val': False
        }
        
        response = client.post(
            '/api/v1/value/',
            json=value_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['tag_id'] == boolean_tag.tag_id
        assert data['boolean_val'] is False
        assert data['name_val'] is None
        assert data['numerical_value'] is None

    def test_create_text_value_success(
        self, client, auth_headers, text_tag
    ):
        """Test POST /api/v1/value/ creates text value"""
        value_data = {
            'tag_id': text_tag.tag_id,
            'name_val': 'Blue'
        }
        
        response = client.post(
            '/api/v1/value/',
            json=value_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['tag_id'] == text_tag.tag_id
        assert data['name_val'] == 'Blue'
        assert data['boolean_val'] is None
        assert data['numerical_value'] is None

    def test_create_numeric_value_success(
        self, client, auth_headers, numeric_tag
    ):
        """Test POST /api/v1/value/ creates numeric value"""
        value_data = {
            'tag_id': numeric_tag.tag_id,
            'numerical_value': 100.5
        }
        
        response = client.post(
            '/api/v1/value/',
            json=value_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['tag_id'] == numeric_tag.tag_id
        assert data['numerical_value'] == 100.5
        assert data['boolean_val'] is None
        assert data['name_val'] is None

    def test_create_value_missing_tag_id(self, client, auth_headers):
        """Test POST /api/v1/value/ fails without tag_id"""
        value_data = {
            'boolean_val': True
        }
        
        response = client.post(
            '/api/v1/value/',
            json=value_data,
            headers=auth_headers
        )
        
        assert response.status_code == 400

    def test_create_value_no_auth(self, client, boolean_tag):
        """Test POST /api/v1/value/ fails without authentication"""
        value_data = {
            'tag_id': boolean_tag.tag_id,
            'boolean_val': True
        }
        
        response = client.post('/api/v1/value/', json=value_data)
        
        assert response.status_code == 401

    def test_update_value_success(
        self, client, auth_headers, boolean_value
    ):
        """Test PUT /api/v1/value/<id> updates value"""
        update_data = {
            'boolean_val': False
        }
        
        response = client.put(
            f'/api/v1/value/{boolean_value.value_id}',
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['value_id'] == boolean_value.value_id
        assert data['boolean_val'] is False

    def test_update_value_change_tag(
        self, client, auth_headers, db_session
    ):
        """Test PUT /api/v1/value/<id> can update tag and values"""
        from app.models import Tag, Value
        
        # Create a tag
        tag = Tag(name='Condition', value_type='text', can_add_new_value=True)
        db_session.add(tag)
        db_session.commit()
        
        # Create a value
        value = Value(tag_id=tag.tag_id, name_val='Good')
        db_session.add(value)
        db_session.commit()
        value_id = value.value_id
        
        # Update the value
        update_data = {
            'name_val': 'Excellent'
        }
        
        response = client.put(
            f'/api/v1/value/{value_id}',
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['name_val'] == 'Excellent'
        assert data['tag_id'] == tag.tag_id

    def test_update_value_not_found(self, client, auth_headers):
        """Test PUT /api/v1/value/<id> with non-existent ID"""
        update_data = {
            'boolean_val': True
        }
        
        response = client.put(
            '/api/v1/value/99999',
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 404

    def test_update_value_no_auth(self, client, boolean_value):
        """Test PUT /api/v1/value/<id> fails without authentication"""
        update_data = {
            'boolean_val': False
        }
        
        response = client.put(
            f'/api/v1/value/{boolean_value.value_id}',
            json=update_data
        )
        
        assert response.status_code == 401

    def test_delete_value_success(
        self, client, auth_headers, boolean_value
    ):
        """Test DELETE /api/v1/value/<id> removes value"""
        value_id = boolean_value.value_id
        
        response = client.delete(
            f'/api/v1/value/{value_id}',
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        
        # Verify value is deleted
        get_response = client.get(f'/api/v1/value/{value_id}')
        assert get_response.status_code == 404

    def test_delete_value_not_found(self, client, auth_headers):
        """Test DELETE /api/v1/value/<id> with non-existent ID"""
        response = client.delete(
            '/api/v1/value/99999',
            headers=auth_headers
        )
        
        assert response.status_code == 404

    def test_delete_value_no_auth(self, client, boolean_value):
        """Test DELETE /api/v1/value/<id> fails without authentication"""
        response = client.delete(
            f'/api/v1/value/{boolean_value.value_id}'
        )
        
        assert response.status_code == 401

    def test_get_values_by_tag(
        self, client, db_session, text_tag
    ):
        """Test GET /api/v1/value/ returns multiple values for same tag"""
        from app.models import Value
        
        # Create multiple values for same tag
        value1 = Value(
            tag_id=text_tag.tag_id,
            name_val='Green'
        )
        value2 = Value(
            tag_id=text_tag.tag_id,
            name_val='Yellow'
        )
        db_session.add(value1)
        db_session.add(value2)
        db_session.commit()
        
        response = client.get('/api/v1/value/')
        
        assert response.status_code == 200
        data = response.get_json()
        
        # Filter values by tag_id
        tag_values = [
            v for v in data if v['tag_id'] == text_tag.tag_id
        ]
        assert len(tag_values) >= 2
        
        names = [v['name_val'] for v in tag_values]
        assert 'Green' in names
        assert 'Yellow' in names

    def test_update_value_partial_update(
        self, client, auth_headers, numeric_value, db_session
    ):
        """Test PUT /api/v1/value/<id> with partial data"""
        original_tag_id = numeric_value.tag_id
        
        # Only update numerical_value
        update_data = {
            'numerical_value': 200.0
        }
        
        response = client.put(
            f'/api/v1/value/{numeric_value.value_id}',
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['numerical_value'] == 200.0
        assert data['tag_id'] == original_tag_id  # Unchanged
