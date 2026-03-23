from django.db import models

# Role: ID (PK), Name, Description
class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'


# Permission: ID (PK), Code, Description
class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'permission'


# RolePermission: ID (PK), Role_ID (FK), Permission_ID (FK)
class RolePermission(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')

    def __str__(self):
        return f'{self.role.name} - {self.permission.code}'

    class Meta:
        db_table = 'role_permission'
        unique_together = ('role', 'permission')


# UserRole: ID (PK), User_ID (FK), Role_ID (FK)
# Note: Using generic 'user_id' instead of FK to allow both Customer and Staff
class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()  # Generic ID - could be Customer or Staff
    user_type = models.CharField(max_length=20)  # 'customer' or 'staff'
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')

    def __str__(self):
        return f'{self.user_type} {self.user_id} - {self.role.name}'

    class Meta:
        db_table = 'user_role'
        unique_together = ('user_id', 'user_type', 'role')
