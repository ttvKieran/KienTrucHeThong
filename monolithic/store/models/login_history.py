from django.db import models

# LoginHistory: ID (PK), Login_Time, IP_Address, User_ID (FK)
# Note: Using generic user_id to support both Customer and Staff
class LoginHistory(models.Model):
    id = models.AutoField(primary_key=True)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_id = models.IntegerField()  # Generic ID - could be Customer or Staff
    user_type = models.CharField(max_length=20)  # 'customer' or 'staff'
    user_agent = models.TextField(blank=True, null=True)
    success = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user_type} {self.user_id} logged in at {self.login_time}'

    class Meta:
        db_table = 'login_history'
        verbose_name_plural = 'Login Histories'
        ordering = ['-login_time']
