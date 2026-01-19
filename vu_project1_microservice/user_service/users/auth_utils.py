"""
JWT Authentication Utilities
"""
import jwt
from datetime import datetime, timedelta
from django.conf import settings


def generate_jwt_token(user):
    """
    Generate JWT token for authenticated user
    
    Args:
        user: User object
    
    Returns:
        str: JWT token
    """
    payload = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token


def decode_jwt_token(token):
    """
    Decode and verify JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        dict: Token payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_user_from_token(request):
    """
    Extract user ID from JWT token in request headers
    
    Args:
        request: Django request object
    
    Returns:
        int: User ID if token is valid, None otherwise
    """
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    payload = decode_jwt_token(token)
    
    if payload:
        return payload.get('user_id')
    
    return None
