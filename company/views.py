from rest_framework import viewsets, filters
from .models import Company
from .permissions import IsActiveEmployee
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    Представление набора данных (CRUD) для модели Company. Включает поиск по стране
    и ограничение на обновление поля 'debt'
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [filters.SearchFilter]
    search_fields = ["country"]

    def perform_update(self, serializer):
        """
        Выполняет обновление объекта при сохранении данных через сериализатор
        """
        # Сохраняем объект, не позволяя изменять значение 'debt'
        serializer.save(debt=self.get_object().debt)
