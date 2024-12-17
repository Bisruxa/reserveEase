import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from Task.models import Task
from rest_framework import filters

class TaskFilter(django_filters.FilterSet):
    # Filters
    status = django_filters.ChoiceFilter(choices=Task.STATUS_CHOICES, empty_label=None)
    priority = django_filters.ChoiceFilter(choices=Task.PRIORITY_CHOICES, empty_label=None)
    due_date = django_filters.DateTimeFilter(field_name='due_date', lookup_expr='gte')  # Tasks with due date >= provided date
    user = django_filters.NumberFilter(field_name='user', lookup_expr='exact')  # Tasks for a specific user
    
    # Sorting based on `sortBy` and `order`
    class Meta:
        model = Task
        fields = ['status', 'priority', 'due_date', 'user']
    
    # Sorting logic
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        
        # Sorting logic
        sort_by = self.request.query_params.get('sortBy', None)
        order = self.request.query_params.get('order', 'asc')  # Default to ascending order
        
        if sort_by:
            if sort_by == 'due_date':
                queryset = queryset.order_by('due_date' if order == 'asc' else '-due_date')
            elif sort_by == 'priority':
                # Custom priority sorting (Low, Medium, High mapped to 1, 2, 3)
                queryset = queryset.order_by('priority' if order == 'asc' else '-priority')
        
        return queryset
