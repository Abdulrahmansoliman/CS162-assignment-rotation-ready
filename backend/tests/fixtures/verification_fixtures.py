"""
Verification Code Fixtures
"""
import pytest
from app.models import VerificationCode, VerificationCodeType
from datetime import datetime, timedelta
from flask import current_app


@pytest.fixture
def registration_code(db_session, user):
    """Create a test verification code.
    
    Default: REGISTRATION type, unused, no attempts.
    """
    now = datetime.utcnow()
    code = VerificationCode(
        user_id=user.user_id,
        code_hash='abc123hash',
        hash_salt='abc123salt',
        code_type=VerificationCodeType.REGISTRATION.code,
        attempts=0,
        is_used=False,
        created_at=now,
        expires_at=now + timedelta(minutes=15)
    )
    db_session.add(code)
    db_session.commit()
    db_session.refresh(code)
    return code


@pytest.fixture
def used_registration_code(db_session, user):
    """Create a used registration code.
    
    Already marked as used with 1 attempt.
    """
    now = datetime.utcnow()
    code = VerificationCode(
        user_id=user.user_id,
        code_hash='used123hash',
        hash_salt='used123salt',
        code_type=VerificationCodeType.REGISTRATION.code,
        attempts=1,
        is_used=True,
        used_at=now,
        created_at=now - timedelta(minutes=10),
        expires_at=now + timedelta(minutes=5)
    )
    db_session.add(code)
    db_session.commit()
    db_session.refresh(code)
    return code


@pytest.fixture
def max_attempts_registration_code(db_session, user, app_context):
    """Create a registration code with max attempts.

    Code has reached maximum attempts and is locked.
    """
    now = datetime.utcnow()
    max_attempts = current_app.config.get('MAX_VERIFICATION_ATTEMPTS', 5)
    code = VerificationCode(
        user_id=user.user_id,
        code_hash='maxattempts123hash',
        hash_salt='maxattempts123salt',
        code_type=VerificationCodeType.REGISTRATION.code,
        attempts=max_attempts,
        is_used=False,
        created_at=now - timedelta(minutes=20),
        expires_at=now + timedelta(minutes=15)
    )
    db_session.add(code)
    db_session.commit()
    db_session.refresh(code)
    return code


@pytest.fixture
def login_code(db_session, verified_user):
    """Create a login verification code.
    
    For an already verified user logging in.
    """
    now = datetime.utcnow()
    code = VerificationCode(
        user_id=verified_user.user_id,
        code_hash='login123hash',
        hash_salt='login123salt',
        code_type=VerificationCodeType.LOGIN.code,
        attempts=0,
        is_used=False,
        created_at=now,
        expires_at=now + timedelta(minutes=15)
    )
    db_session.add(code)
    db_session.commit()
    db_session.refresh(code)
    return code


@pytest.fixture
def expired_registration_code(db_session, user):
    """Create an expired registration code.

    Code is past its expiration time.
    """
    now = datetime.utcnow()
    code = VerificationCode(
        user_id=user.user_id,
        code_hash='expired123hash',
        hash_salt='expired123salt',
        code_type=VerificationCodeType.REGISTRATION.code,
        attempts=0,
        is_used=False,
        created_at=now - timedelta(minutes=30),
        expires_at=now - timedelta(minutes=5)  # Already expired
    )
    db_session.add(code)
    db_session.commit()
    db_session.refresh(code)
    return code

@pytest.fixture
def expired_login_code(db_session, verified_user):
    """Create an expired login code.

    Code is past its expiration time.
    """
    now = datetime.utcnow()
    code = VerificationCode(
        user_id=verified_user.user_id,
        code_hash='expiredlogin123hash',
        hash_salt='expiredlogin123salt',
        code_type=VerificationCodeType.LOGIN.code,
        attempts=0,
        is_used=False,
        created_at=now - timedelta(minutes=30),
        expires_at=now - timedelta(minutes=5)  # Already expired
    )
    db_session.add(code)
    db_session.commit()
    db_session.refresh(code)
    return code

@pytest.fixture
def used_login_code(db_session, verified_user):
    """Create a used login code.
    
    Already marked as used with 1 attempt.
    """
    now = datetime.utcnow()
    code = VerificationCode(
        user_id=verified_user.user_id,
        code_hash='usedlogin123hash',
        hash_salt='usedlogin123salt',
        code_type=VerificationCodeType.LOGIN.code,
        attempts=1,
        is_used=True,
        used_at=now,
        created_at=now - timedelta(minutes=10),
        expires_at=now + timedelta(minutes=5)
    )
    db_session.add(code)
    db_session.commit()
    db_session.refresh(code)
    return code

@pytest.fixture
def max_attempts_login_code(db_session, verified_user, app_context):
    """Create a login code with max attempts.

    Code has reached maximum attempts and is locked.
    """
    now = datetime.utcnow()
    max_attempts = current_app.config.get('MAX_VERIFICATION_ATTEMPTS', 5)
    code = VerificationCode(
        user_id=verified_user.user_id,
        code_hash='maxattemptslogin123hash',
        hash_salt='maxattemptslogin123salt',
        code_type=VerificationCodeType.LOGIN.code,
        attempts=max_attempts,
        is_used=False,
        created_at=now - timedelta(minutes=20),
        expires_at=now + timedelta(minutes=15)
    )
    db_session.add(code)
    db_session.commit()
    db_session.refresh(code)
    return code