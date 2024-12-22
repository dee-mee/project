from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Recipe, UserTry
from .serializers import RecipeSerializer
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import UserHistory

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
    """Display recipes filtered by location and optionally ingredients."""
    # Get location and ingredients from request
    location = request.GET.get('location', '')
    ingredients = request.GET.get('ingredients', '').split(',')

    # Query recipes filtered by location and ingredients
    recipes = Recipe.objects.all()
    if location:
        recipes = recipes.filter(location__name__icontains=location)
    if ingredients:
        recipes = recipes.filter(ingredients__name__in=ingredients).distinct()

    return render(request, 'recipes/homepage.html', {'recipes': recipes, 'location': location})


def download_recipe(request, recipe_id):
    """Generate and return a PDF for a specific recipe."""
    # Get the recipe from the database
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Create an HTTP response with the appropriate content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{recipe.title}.pdf"'

    # Use ReportLab to generate the PDF
    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, f"Recipe: {recipe.title}")
    p.setFont("Helvetica", 12)
    p.drawString(100, 780, f"Preparation Time: {recipe.prep_time} minutes")
    p.drawString(100, 760, "Ingredients:")

    # List ingredients
    y = 740
    for ingredient in recipe.ingredients.all():
        p.drawString(120, y, f"- {ingredient.name}")
        y -= 20

    # Add instructions
    p.drawString(100, y - 20, "Instructions:")
    y -= 40
    for line in recipe.instructions.split('\n'):
        p.drawString(120, y, line)
        y -= 20

    # Finalize the PDF
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
@login_required
def recipe_detail(request, recipe_id):
    """Render a detailed page for a specific recipe."""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/recipe_page.html', {'recipe': recipe})

def all_recipes(request):
    """Render a page with a list of all recipes."""
    recipes = Recipe.objects.all()
    return render(request, 'recipes/all_recipes.html', {'recipes': recipes})

# Profile
@login_required
def profile(request):
    """Render the user's profile page."""
    user_email = request.user.email if request.user.is_authenticated else 'guest@example.com'
    user_history = Recipe.objects.filter(usertry__user_email=user_email)
    return render(request, 'recipes/profile.html', {'user_history': user_history})

@login_required
def profile_view(request):
    user = request.user
    # If you have a custom profile model, retrieve additional fields
    context = {
        'name': user.get_full_name(),  # Or `user.username` for the username
        'email': user.profile.email,       # Assuming you have an 'age' field in the profile model
        'location': user.profile.location,  # Assuming you have a 'location' field
    }
    return render(request, 'recipes/profile.html', context)

#history page
@login_required
def history_view(request):
    # Get history for the logged-in user
    user_history = UserHistory.objects.filter(user=request.user).order_by('-timestamp')

    # Pass the history data to the template
    context = {
        'name': request.user.get_full_name() or request.user.username,
        'history': user_history,
    }
    return render(request, 'recipes/history.html', context)

# Contact
def contact_view(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # You can process the form data here (e.g., save to the database or send an email)
        # Example: print the submitted data
        print(f"Name: {name}, Email: {email}, Message: {message}")

        # Optionally, add a success message
        messages.success(request, "Your message has been sent successfully!")

        # Redirect to the homepage
        return redirect('homepage')

    # Render the contact form for GET requests
    return render(request, 'recipes/contact.html')

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