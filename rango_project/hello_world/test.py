from django.test import TestCase
from hello_world.models import category
from django.urls import reverse

class CategoryMethodTest(TestCase):
    def test_ensure_views_are_positive(self):
        cat = category(name='test',views=1,likes=0)
        cat.save()
        self.assertEqual((cat.views>0),True)

    
def add_cat(name, views, likes):
    c = category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        response = self.client.get(reverse('index')) 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.") 
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        add_cat('test',1,1)
        add_cat('temp',1,1)
        add_cat('tmp',1,1)
        add_cat('tmp test temp',1,1)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")
        num_cats =len(response.context['categories'])
        self.assertEqual(num_cats , 4)
