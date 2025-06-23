from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from .forms import WallPaintCalculatorForm, FlooringCalculatorForm
import os
from .products import Product, PaintProduct

script_dir = os.path.dirname(os.path.abspath(__file__))
paints = []
choices = []

def calc_price_from_sizes(product_sizes, litres):
    cost = 0
    sizes = []
    prices = []

    for p in product_sizes:
        match p.size:
            case "500ML":
                sizes.append(0.5)
            case "1L":
                sizes.append(1.0)
            case "2L":
                sizes.append(2.0)
            case "4L":
                sizes.append(4.0)
            case "10L":
                sizes.append(10.0)
            case "15L":
                sizes.append(15.0)
            case "20L":
                sizes.append(20.0)
        prices.append(float(p.price))

    min_size = sizes[0]
    sizes.sort(reverse=True)
    prices.sort(reverse=True)
    sizes_needed = []

    # get sizes needed for litre amount
    while litres > 0:
        for s in sizes:
            if s <= litres + min_size:
                litres -= s
                sizes_needed.append(s)
                print(litres)
                break
        print(litres)

    # Get prices from product sizes
    for s in sizes_needed:
        cost += prices[sizes.index(s)]
    
    return f"Cost: ${cost}, Sizes needed: {str(sizes_needed).replace("[", "").replace("]", "")}"

def calculate_wall_paint(request):
    litres_needed = None
    cost = None
    choice_id = 0
    choices = []
    
    # Open scraped paints file and put details into a list of paint products
    with open(f"{script_dir}/product_details/paint.txt", "r") as f:
        for line in f:
            # put details of product into list
            details = line.split("\t")

            # create new paint product
            paint = PaintProduct(details[0], details[2], details[3], details[1])

            # add product to paints list
            found_paint = False
            for p in paints:
                for size in p:
                    if paint.name == size.name:
                        found_paint = True
                        p.append(paint)
                        break

            if not found_paint:
                product = []
                paints.append(product)
                product.append(paint)

            # create choice item for dropdown
            # choice = [details[0].lower().replace(" ", "-").replace("®", "").replace("™", "").replace("+", "").replace("&", ""), details[0]]

            choice = [str(choice_id), details[0]]
            choice2 = [str(choice_id - 1), details[0]]

            # if choice not found in choice list, add it
            if choice2 not in choices:
                choices.append(choice)
                choice_id += 1

    # When user clicks "calculate", get values from form and calculate litres needed and cost
    if request.method == ("POST"):
        form_wall_paint = WallPaintCalculatorForm(request.POST)
        form_wall_paint.fields["product"].choices = choices
        if form_wall_paint.is_valid():
            perimeter = form_wall_paint.cleaned_data["perimeter"]
            height = form_wall_paint.cleaned_data["height"]
            sq_per_litre = form_wall_paint.cleaned_data["sq_per_litre"]
            num_coats = form_wall_paint.cleaned_data["num_coats"]
            litres_needed = (num_coats * perimeter * height) / sq_per_litre
            selection_index = form_wall_paint.cleaned_data["product"][0]
            print(selection_index)
            cost = calc_price_from_sizes(paints[int(form_wall_paint.cleaned_data["product"][0])], float(litres_needed))
            
    else:  # On load page
        form_wall_paint = WallPaintCalculatorForm()
        # form_wall_paint.fields["cost_per_litre"].initial = float(paints[0][0].price)
        form_wall_paint.fields["product"].choices = choices

    return render(request, "paint.html", {"form_wall_paint": form_wall_paint, "litres_needed": litres_needed, "cost_wall_paint": cost, "paints": paints, "choices": choices})

def calc_flooring(request):
    sq_m = None
    cost_flooring = None

    if request.method == ("POST"):
        form_flooring = FlooringCalculatorForm(request.POST)
        if form_flooring.is_valid():
            length = form_flooring.cleaned_data["length"]
            width = form_flooring.cleaned_data["width"]
            cost_per_sq = form_flooring.cleaned_data["cost_per_sq"]
            sq_m = length * width
            cost_flooring = sq_m * cost_per_sq
    else:
        form_flooring = FlooringCalculatorForm()

    return render(request, "flooring.html", {"form_flooring": form_flooring, "sq_m": sq_m, "cost_flooring": cost_flooring})

def calc_plaster(request):
    return render(request, "plaster.html")

# Create your views here.
def index(request):
    return render(request, "index.html")

def render_page(request):
    wall_paint = calculate_wall_paint()
    flooring = calc_flooring()
    return render(request, "paint.html", {"x": wall_paint})