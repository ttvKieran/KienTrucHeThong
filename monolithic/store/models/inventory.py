from django.db import models

# Supplier: ID (PK), Name, Phone, Email
class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'supplier'


# Import: ID (PK), Import_Date, Total_Cost, Staff_ID (FK), Supplier_ID (FK)
class Import(models.Model):
    id = models.AutoField(primary_key=True)
    import_date = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return f'Import {self.id} from {self.supplier.name}'

    class Meta:
        db_table = 'import'


# ImportDetail: ID (PK), Quantity, Import_Price, Import_ID (FK), Book_ID (FK)
class ImportDetail(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    import_price = models.DecimalField(max_digits=10, decimal_places=2)
    import_record = models.ForeignKey(Import, on_delete=models.CASCADE, related_name='details')
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

    def __str__(self):
        return f'Import Detail {self.id} - {self.book.title}'

    class Meta:
        db_table = 'import_detail'


# Warehouse: ID (PK), Name, Location
class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'warehouse'


# Inventory: ID (PK), Quantity, Book_ID (FK), Warehouse_ID (FK)
class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.book.title} - {self.quantity} units in {self.warehouse.name}'

    class Meta:
        db_table = 'inventory'
        verbose_name_plural = 'Inventories'
        unique_together = ('book', 'warehouse')


# StockMovement: ID (PK), Type, Quantity, Created_At
class StockMovement(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)  # 'in' or 'out'
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.type.upper()} - {self.quantity} units'

    class Meta:
        db_table = 'stock_movement'


# StockIn: ID (PK), Import_ID (FK), Stock_Movement_ID (FK)
class StockIn(models.Model):
    id = models.AutoField(primary_key=True)
    import_record = models.ForeignKey(Import, on_delete=models.CASCADE)
    stock_movement = models.OneToOneField(StockMovement, on_delete=models.CASCADE)

    def __str__(self):
        return f'Stock In {self.id} from Import {self.import_record.id}'

    class Meta:
        db_table = 'stock_in'


# StockOut: ID (PK), Order_ID (FK), Stock_Movement_ID (FK)
class StockOut(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    stock_movement = models.OneToOneField(StockMovement, on_delete=models.CASCADE)

    def __str__(self):
        return f'Stock Out {self.id} for Order {self.order.id}'

    class Meta:
        db_table = 'stock_out'


# DamageReport: ID (PK), Reason, Quantity, Book_ID (FK)
class DamageReport(models.Model):
    id = models.AutoField(primary_key=True)
    reason = models.TextField()
    quantity = models.IntegerField()
    reported_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Damage Report {self.id} - {self.book.title}'

    class Meta:
        db_table = 'damage_report'


# InventoryAudit: ID (PK), Audit_Date, Staff_ID (FK)
class InventoryAudit(models.Model):
    id = models.AutoField(primary_key=True)
    audit_date = models.DateTimeField(auto_now_add=True)
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Audit {self.id} by {self.staff.name} on {self.audit_date}'

    class Meta:
        db_table = 'inventory_audit'
