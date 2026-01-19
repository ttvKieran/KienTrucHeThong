"""
Service Communication - Interact with other microservices
"""
import requests
from django.conf import settings


class BookServiceClient:
    """Client for communicating with Book Service"""
    
    @staticmethod
    def get_book_details(book_id):
        """
        Get book details from Book Service
        
        Args:
            book_id: Book ID
        
        Returns:
            dict: Book details or None if not found
        """
        try:
            url = f"{settings.BOOK_SERVICE_URL}/api/books/{book_id}/"
            response = requests.get(url, timeout=settings.SERVICE_REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                return response.json()
            return None
            
        except requests.RequestException:
            return None
    
    @staticmethod
    def check_stock(book_id, quantity):
        """
        Check if book has sufficient stock
        
        Args:
            book_id: Book ID
            quantity: Requested quantity
        
        Returns:
            dict: Stock check result or None if error
        """
        try:
            url = f"{settings.BOOK_SERVICE_URL}/api/books/check-stock/"
            data = {'book_id': book_id, 'quantity': quantity}
            response = requests.post(
                url,
                json=data,
                timeout=settings.SERVICE_REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            return None
            
        except requests.RequestException:
            return None
    
    @staticmethod
    def update_stock(book_id, quantity, operation='decrease'):
        """
        Update book stock (increase or decrease)
        
        Args:
            book_id: Book ID
            quantity: Quantity to update
            operation: 'increase' or 'decrease'
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            url = f"{settings.BOOK_SERVICE_URL}/api/books/{book_id}/stock/"
            data = {'quantity': quantity, 'operation': operation}
            response = requests.post(
                url,
                json=data,
                timeout=settings.SERVICE_REQUEST_TIMEOUT
            )
            
            return response.status_code == 200
            
        except requests.RequestException:
            return False


class UserServiceClient:
    """Client for communicating with User Service"""
    
    @staticmethod
    def get_user_details(user_id):
        """
        Get user details from User Service
        
        Args:
            user_id: User ID
        
        Returns:
            dict: User details or None if not found
        """
        try:
            url = f"{settings.USER_SERVICE_URL}/api/users/{user_id}/"
            response = requests.get(url, timeout=settings.SERVICE_REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                return response.json()
            return None
            
        except requests.RequestException:
            return None
