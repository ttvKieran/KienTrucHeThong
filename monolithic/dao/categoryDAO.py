from store.models import Category


class CategoryDAO:
    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    
    @staticmethod
    def get_category_by_id(category_id):
        return Category.objects.get(id=category_id)
    
    @staticmethod
    def create_category(name, description=''):
        return Category.objects.create(
            name=name,
            description=description
        )
    
    @staticmethod
    def update_category(category_id, name=None, description=None):
        category = Category.objects.get(id=category_id)
        
        if name is not None:
            category.name = name
        if description is not None:
            category.description = description
            
        category.save()
        return category
    
    @staticmethod
    def delete_category(category_id):
        category = Category.objects.get(id=category_id)
        category.delete()
        return True
    
    @staticmethod
    def search_categories_by_name(name):
        return Category.objects.filter(name__icontains=name)
    
    @staticmethod
    def category_exists(category_id):
        return Category.objects.filter(id=category_id).exists()
    
    @staticmethod
    def count_categories():
        return Category.objects.count()
