from django.db import models

class EmployeeSalary(models.Model):
    city = models.CharField(max_length=100)
    plant_code = models.CharField(max_length=100)
    division = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.city} - {self.salary}"

class SalaryData(models.Model):
    city = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.salary} (Добавлено: {self.date_added})"
