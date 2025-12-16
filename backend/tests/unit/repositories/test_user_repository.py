import pytest
from app.repositories.implementations.user_repository import UserRepository
from app.models.user import User
from app.models.verification_stutus_enum import VerificationStatusEnum


@pytest.mark.unit
@pytest.mark.repository
class TestUserRepository:

    @pytest.fixture
    def repository(self):
        return UserRepository()

    def test_get_user_by_email_when_user_exists(
        self,
        db_session,
        repository,
        user
    ):
        result = repository.get_user_by_email(user.email)
        
        assert result is not None
        assert result.user_id == user.user_id
        assert result.email == user.email

    def test_get_user_by_email_when_user_does_not_exist(
        self,
        db_session,
        repository
    ):
        result = repository.get_user_by_email("nonexistent@example.com")
        
        assert result is None

    def test_create_user_with_valid_data(
        self,
        db_session,
        repository,
        rotation_city
    ):
        user = repository.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            rotation_city_id=rotation_city.city_id
        )
        
        assert user is not None
        assert user.user_id is not None
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.rotation_city_id == rotation_city.city_id
        assert user.is_verified is False
        assert user.status == VerificationStatusEnum.PENDING.code

    def test_create_user_persists_to_database(
        self,
        db_session,
        repository,
        rotation_city
    ):
        user = repository.create_user(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            rotation_city_id=rotation_city.city_id
        )
        
        db_session.expire_all()
        persisted_user = db_session.get(User, user.user_id)
        
        assert persisted_user is not None
        assert persisted_user.email == "jane.smith@example.com"

    def test_mark_user_as_verified_when_user_exists(
        self,
        db_session,
        repository,
        user
    ):
        result = repository.mark_user_as_verified(user.user_id)
        
        assert result is not None
        assert result.is_verified is True
        assert result.status == VerificationStatusEnum.VERIFIED.code

    def test_mark_user_as_verified_persists_changes(
        self,
        db_session,
        repository,
        user
    ):
        repository.mark_user_as_verified(user.user_id)
        
        db_session.expire_all()
        persisted_user = db_session.get(User, user.user_id)
        
        assert persisted_user.is_verified is True
        assert persisted_user.status == VerificationStatusEnum.VERIFIED.code

    def test_mark_user_as_verified_when_user_does_not_exist(
        self,
        db_session,
        repository
    ):
        result = repository.mark_user_as_verified(99999)
        
        assert result is None

    def test_get_user_by_id_when_user_exists(
        self,
        db_session,
        repository,
        user
    ):
        result = repository.get_user_by_id(user.user_id)
        
        assert result is not None
        assert result.user_id == user.user_id

    def test_get_user_by_id_when_user_does_not_exist(
        self,
        db_session,
        repository
    ):
        result = repository.get_user_by_id(99999)
        
        assert result is None

    def test_get_all_users_returns_empty_list_when_no_users(
        self,
        db_session,
        repository
    ):
        result = repository.get_all_users()
        
        assert isinstance(result, list)
        assert len(result) == 0

    def test_get_all_users_returns_all_users(
        self,
        db_session,
        repository,
        rotation_city
    ):
        repository.create_user(
            first_name="User1",
            last_name="Test1",
            email="user1@example.com",
            rotation_city_id=rotation_city.city_id
        )
        repository.create_user(
            first_name="User2",
            last_name="Test2",
            email="user2@example.com",
            rotation_city_id=rotation_city.city_id
        )
        
        result = repository.get_all_users()
        
        assert len(result) == 2
        assert all(isinstance(u, User) for u in result)

    def test_update_user_with_single_field(
        self,
        db_session,
        repository,
        user
    ):
        updated_user = repository.update(
            user.user_id,
            first_name="UpdatedName"
        )
        
        assert updated_user.first_name == "UpdatedName"
        assert updated_user.last_name == user.last_name

    def test_update_user_with_multiple_fields(
        self,
        db_session,
        repository,
        user
    ):
        updated_user = repository.update(
            user.user_id,
            first_name="NewFirst",
            last_name="NewLast",
            rotation_city_id=user.rotation_city_id
        )
        
        assert updated_user.first_name == "NewFirst"
        assert updated_user.last_name == "NewLast"
        assert updated_user.rotation_city_id == user.rotation_city_id

    def test_update_user_persists_changes(
        self,
        db_session,
        repository,
        user
    ):
        repository.update(user.user_id, first_name="Persisted")
        
        db_session.expire_all()
        persisted_user = db_session.get(User, user.user_id)
        
        assert persisted_user.first_name == "Persisted"

    def test_update_user_raises_error_when_user_not_found(
        self,
        db_session,
        repository
    ):
        with pytest.raises(ValueError, match="User not found"):
            repository.update(99999, first_name="Test")

    def test_update_user_ignores_invalid_attributes(
        self,
        db_session,
        repository,
        user
    ):
        updated_user = repository.update(
            user.user_id,
            invalid_field="should_be_ignored",
            first_name="ValidUpdate"
        )
        
        assert updated_user.first_name == "ValidUpdate"
        assert not hasattr(updated_user, "invalid_field")


    def test_create_user_with_profile_picture(self, db_session, rotation_city, repository):
        pic = "data:image/png;base64,TESTBASE64DATA"

        user = repository.create_user(
            first_name="Pic",
            last_name="User",
            email="pic@example.com",
            rotation_city_id=rotation_city.city_id,
            profile_picture=pic,
        )

        assert user is not None
        assert user.profile_picture == pic

        db_session.expire_all()
        persisted = db_session.get(User, user.user_id)
        assert persisted.profile_picture == pic

    def test_update_user_profile_picture(self, db_session, user, repository):
        pic = "data:image/jpeg;base64,OTHERBASE64DATA"

        updated = repository.update(user.user_id, profile_picture=pic)

        assert updated.profile_picture == pic

        db_session.expire_all()
        persisted = db_session.get(User, user.user_id)
        assert persisted.profile_picture == pic


    def test_update_user_removes_profile_picture(self, db_session, user_with_profile_picture, repository):

        # Now remove it
        updated = repository.update(user_with_profile_picture.user_id, profile_picture=None)

        assert updated.profile_picture is None

        db_session.expire_all()
        persisted = db_session.get(User, user_with_profile_picture.user_id)
        assert persisted.profile_picture is None

    def test_create_user_with_profile_picture_none(self, db_session, rotation_city, repository):
        user = repository.create_user(
            first_name="NoPic",
            last_name="User",
            email="nopicture@example.com",
            rotation_city_id=rotation_city.city_id,
            profile_picture=None
        )

        assert user is not None
        assert user.profile_picture is None

        db_session.expire_all()
        persisted = db_session.get(User, user.user_id)
        assert persisted.profile_picture is None