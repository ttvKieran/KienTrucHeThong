"""
API Gateway Views - Proxy requests to microservices
"""
import requests
import jwt
from datetime import datetime
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'service': 'api-gateway',
        'timestamp': datetime.now().isoformat()
    })


class ServiceProxy(APIView):
    """
    Base proxy class for forwarding requests to microservices
    """
    service_url = None
    
    def get_auth_header(self, request):
        """Extract and validate JWT token from request"""
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                # Verify token
                payload = jwt.decode(
                    token, 
                    settings.JWT_SECRET_KEY, 
                    algorithms=[settings.JWT_ALGORITHM]
                )
                return {'Authorization': f'Bearer {token}'}, payload
            except jwt.ExpiredSignatureError:
                return None, {'error': 'Token expired'}
            except jwt.InvalidTokenError:
                return None, {'error': 'Invalid token'}
        return {}, None
    
    def forward_request(self, request, endpoint, method='GET', **kwargs):
        """
        Forward request to microservice
        """
        if not self.service_url:
            return Response(
                {'error': 'Service URL not configured'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        url = f"{self.service_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        # Add auth header if present
        auth_header, auth_payload = self.get_auth_header(request)
        if auth_payload and 'error' in auth_payload:
            return Response(auth_payload, status=status.HTTP_401_UNAUTHORIZED)
        
        headers.update(auth_header)
        
        # Add user_id to params if authenticated
        params = kwargs.get('params', {})
        if auth_payload and 'user_id' in auth_payload:
            params['user_id'] = auth_payload['user_id']
            kwargs['params'] = params
        
        try:
            if method == 'GET':
                response = requests.get(
                    url, 
                    headers=headers,
                    params=kwargs.get('params'),
                    timeout=settings.SERVICE_REQUEST_TIMEOUT
                )
            elif method == 'POST':
                response = requests.post(
                    url,
                    headers=headers,
                    json=kwargs.get('data'),
                    timeout=settings.SERVICE_REQUEST_TIMEOUT
                )
            elif method == 'PUT':
                response = requests.put(
                    url,
                    headers=headers,
                    json=kwargs.get('data'),
                    timeout=settings.SERVICE_REQUEST_TIMEOUT
                )
            elif method == 'DELETE':
                response = requests.delete(
                    url,
                    headers=headers,
                    timeout=settings.SERVICE_REQUEST_TIMEOUT
                )
            else:
                return Response(
                    {'error': 'Method not supported'},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED
                )
            
            # Return response from microservice
            return Response(
                response.json() if response.content else {},
                status=response.status_code
            )
            
        except requests.Timeout:
            return Response(
                {'error': f'Service timeout: {self.service_url}'},
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )
        except requests.ConnectionError:
            return Response(
                {'error': f'Service unavailable: {self.service_url}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            return Response(
                {'error': f'Gateway error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserServiceProxy(ServiceProxy):
    """Proxy for User Service"""
    service_url = settings.USER_SERVICE_URL
    
    def post(self, request):
        """Handle POST requests (register, login)"""
        path = request.path
        
        if 'register' in path:
            return self.forward_request(
                request, 
                '/api/users/register/',
                method='POST',
                data=request.data
            )
        elif 'login' in path:
            return self.forward_request(
                request,
                '/api/users/login/',
                method='POST',
                data=request.data
            )
        
        return Response(
            {'error': 'Endpoint not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    def get(self, request):
        """Handle GET requests (profile)"""
        return self.forward_request(
            request,
            '/api/users/profile/',
            method='GET'
        )
    
    def put(self, request):
        """Handle PUT requests (update profile)"""
        return self.forward_request(
            request,
            '/api/users/profile/',
            method='PUT',
            data=request.data
        )


class BookServiceProxy(ServiceProxy):
    """Proxy for Book Service"""
    service_url = settings.BOOK_SERVICE_URL
    
    def get(self, request, book_id=None):
        """Handle GET requests (list books, get book detail)"""
        if book_id:
            return self.forward_request(
                request,
                f'/api/books/{book_id}/',
                method='GET'
            )
        else:
            return self.forward_request(
                request,
                '/api/books/',
                method='GET',
                params=request.query_params
            )
    
    def post(self, request):
        """Handle POST requests (create book - admin only)"""
        return self.forward_request(
            request,
            '/api/books/',
            method='POST',
            data=request.data
        )
    
    def put(self, request, book_id):
        """Handle PUT requests (update book - admin only)"""
        return self.forward_request(
            request,
            f'/api/books/{book_id}/',
            method='PUT',
            data=request.data
        )
    
    def delete(self, request, book_id):
        """Handle DELETE requests (delete book - admin only)"""
        return self.forward_request(
            request,
            f'/api/books/{book_id}/',
            method='DELETE'
        )


class CartServiceProxy(ServiceProxy):
    """Proxy for Cart Service"""
    service_url = settings.CART_SERVICE_URL
    
    def get(self, request):
        """Handle GET requests (view cart)"""
        return self.forward_request(
            request,
            '/api/cart/',
            method='GET'
        )
    
    def post(self, request):
        """Handle POST requests (add to cart, checkout)"""
        path = request.path
        
        if 'add' in path:
            return self.forward_request(
                request,
                '/api/cart/add/',
                method='POST',
                data=request.data
            )
        elif 'checkout' in path:
            return self.forward_request(
                request,
                '/api/cart/checkout/',
                method='POST',
                data=request.data
            )
        
        return Response(
            {'error': 'Endpoint not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    def put(self, request):
        """Handle PUT requests (update cart item)"""
        return self.forward_request(
            request,
            '/api/cart/update/',
            method='PUT',
            data=request.data
        )
    
    def delete(self, request, book_id):
        """Handle DELETE requests (remove from cart)"""
        return self.forward_request(
            request,
            f'/api/cart/remove/{book_id}/',
            method='DELETE'
        )
