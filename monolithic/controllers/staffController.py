from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from store.models import Staff

# API: Lấy danh sách nhân viên
@require_http_methods(["GET"])
def list_staff(request):
    """Lấy danh sách tất cả nhân viên"""
    staff = Staff.objects.all()
    data = [{
        'id': s.id,
        'name': s.name,
        'role': s.role
    } for s in staff]
    return JsonResponse(data, safe=False)

# API: Lấy thông tin một nhân viên
@require_http_methods(["GET"])
def get_staff(request, staff_id):
    """Lấy thông tin một nhân viên"""
    try:
        staff = Staff.objects.get(id=staff_id)
        return JsonResponse({
            'id': staff.id,
            'name': staff.name,
            'role': staff.role
        })
    except Staff.DoesNotExist:
        return JsonResponse({'error': 'Staff not found'}, status=404)
