from django.test import TestCase
from django.urls import reverse,resolve
from recipes import views
from recipes.models import Category, Recipe, User

class RecipeViewsTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home-workout'))
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id':1000}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1000}))
        self.assertEqual(response.status_code,404)

    def test_recipe_home_template_shows_no_recipe_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home-workout'))
        self.assertIn('Nada para ver aqui😢', response.content.decode('utf-8'))

    def test_recipe_home_templates_loads_recipes(self):
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name = 'user',
            last_name = 'name',
            username= 'username',
            password='123456',
            email='username@gmail.com'
        )
        recipe = Recipe.objects.create(
            category = category,
            author = author,
            title = 'Recipe Title',
            description = 'Recipe Description',
            slug = 'recipe-slug',
            preparation_time = 10,
            preparation_time_unit = 'Minutos',
            servings = 5,
            servings_unit = 'porções',
            preparation_steps = 'Preparation Steps',
            preparation_steps_is_html = False,
            is_published = True,
            )
        response = self.client.get(reverse('recipes:home-workout'))
        response_recipes = response.context['recipes']

        self.assertEqual(response_recipes.first().title, 'Recipe Title')

        pass
    def test_recipe_card_view_function_is_correct(self):
        view = resolve(reverse('recipes:card-training', kwargs={'id':1}))
        self.assertIs(view.func, views.card_training)

    def test_recipe_card_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:card-training', kwargs={'id':1000}))
        self.assertEqual(response.status_code,404)

    def test_recipe_home_view_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home-workout'))
        self.assertEqual(response.status_code,200)
    
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home-workout'))
        self.assertTemplateUsed(response,'recipes/pages/home.html')

    def test_recipe_search_uses_correct_view(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)
    
    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertTemplateUsed(response,'recipes/pages/search.html')
    
    def test_recipe_search_raiser_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)