from django.db import models

# Staff: ID (PK), Name, Email, Password, Role.
class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, default='staff@bookstore.com')
    password = models.CharField(max_length=100, default='123456')
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.role}"