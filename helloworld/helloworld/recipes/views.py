from django.shortcuts import render

RECIPES = {
    "goulash": "Гуляш: мясо, лук, морковь, томатная паста, специи.",
    "dumplings": "Вареники: тесто, картофель, сыр, сметана.",
    "pasta": "Паста: спагетти, томаты, чеснок, базилик.",
    "borscht": "Борщ: капуста, свекла, картофель, мясо, сметана.",
}

def recipe_view(request):
    recipe_name = request.GET.get('recipe', '').lower()
    recipe = RECIPES.get(recipe_name, "Рецепт не найден. Попробуйте другой запрос.")

    context = {
        'recipe_name': recipe_name.capitalize() if recipe_name else None,
        'recipe': recipe,
    }
    return render(request, 'recipe_view.html', context)
