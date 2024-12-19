from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Recipe, UserTry
from .serializers import RecipeSerializer
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import get_object_or_404


# Create your views here.


class RecipeListView(APIView):
    """API endpoint to fetch recipes based on filters."""
    def get(self, request):
        location = request.query_params.get('location')
        ingredients = request.query_params.getlist('ingredients')
        recipes = Recipe.objects.filter(
            location__name__icontains=location,
            ingredients__name__in=ingredients
        ).distinct()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

def homepage(request):
    """Render the homepage with recipe recommendations."""
    location = request.GET.get('location', 'Default Location')
    recipes = Recipe.objects.filter(location__name__icontains=location)
    return render(request, 'recipes/homepage.html', {'recipes': recipes, 'location': location})


def download_recipe(request, recipe_id):
    """Generates a PDF for a specific recipe and sends it as a response."""
    # Fetch the recipe from the database
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Create an HTTP response with PDF headers
    response = FileResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{recipe.title}.pdf"'

    # Use ReportLab to generate the PDF content
    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)
    p.drawString(100, 800, f"Recipe: {recipe.title}")
    p.drawString(100, 780, f"Ingredients: {', '.join([i.name for i in recipe.ingredients.all()])}")
    p.drawString(100, 760, "Instructions:")
    p.drawString(100, 740, recipe.instructions[:200])  # Display the first 200 characters

    # Finalize and close the PDF
    p.showPage()
    p.save()

    return response


#landing page
def landing_page(request):
    """Render the landing page."""
    return render(request, 'recipes/landing_page.html')


# Homepage
def homepage(request):
    """Render the homepage with recipe recommendations."""
    location = request.GET.get('location', 'Default Location')
    recipes = Recipe.objects.filter(location__name__icontains=location)
    return render(request, 'recipes/homepage.html', {'recipes': recipes, 'location': location})

# Recipe Detail
def recipe_detail(request, recipe_id):
    """Render a detailed page for a specific recipe."""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/recipe_page.html', {'recipe': recipe})

# Profile
def profile(request):
    """Render the user's profile page."""
    user_email = request.user.email if request.user.is_authenticated else 'guest@example.com'
    user_history = Recipe.objects.filter(usertry__user_email=user_email)
    return render(request, 'recipes/profile.html', {'user_history': user_history})

#history page
def history(request):
    """Render the history page with recipes the user has tried."""
    user_email = request.user.email if request.user.is_authenticated else "guest@example.com"
    user_history = UserTry.objects.filter(user_email=user_email)
    return render(request, 'recipes/history.html', {'user_history': user_history})


# Contact
def contact(request):
    """Render the contact page and handle form submission."""
    if request.method == 'POST':
        # Process the form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Logic to handle the message (e.g., send an email)
        return render(request, 'recipes/contact.html', {'success': True})
    return render(request, 'recipes/contact.html')

# About Page (Optional)
def about(request):
    """Render the about page."""
    return render(request, 'recipes/about.html')


def signup(request):
    """Handle user signup."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'recipes/signup.html', {'form': form})