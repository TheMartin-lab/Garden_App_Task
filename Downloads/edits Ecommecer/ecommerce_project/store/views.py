from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .models import Store, Product, Order, OrderItem, Review
from .forms import UserRegistrationForm, StoreForm, ProductForm, ReviewForm
from .cart import Cart
from .twitter import tweet_store, tweet_product

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'store/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('product_list')

def product_list(request):
    if request.user.is_authenticated:
        Order.objects.filter(user=request.user, is_paid=False).delete()
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# Vendor Views

@login_required
def my_stores(request):
    if not request.user.is_vendor:
        messages.error(request, "You are not a vendor.")
        return redirect('product_list')
    stores = request.user.stores.all()
    return render(request, 'store/my_stores.html', {'stores': stores})

@login_required
def add_store(request):
    if not request.user.is_vendor:
        messages.error(request, "You are not a vendor.")
        return redirect('product_list')
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()
            try:
                tweet_store(store)
            except Exception:
                pass
            return redirect('my_stores')
    else:
        form = StoreForm()
    return render(request, 'store/add_store.html', {'form': form})

@login_required
def edit_store(request, store_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            return redirect('my_stores')
    else:
        form = StoreForm(instance=store)
    return render(request, 'store/edit_store.html', {'form': form, 'store': store})

@login_required
def delete_store(request, store_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    if request.method == 'POST':
        store.delete()
        return redirect('my_stores')
    return render(request, 'store/delete_store.html', {'store': store})

@login_required
def store_products(request, store_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    products = store.products.all()
    return render(request, 'store/store_products.html', {'store': store, 'products': products})

@login_required
def adjust_inventory(request, store_id, product_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    product = get_object_or_404(Product, id=product_id, store=store)
    if request.method == 'POST':
        action = request.POST.get('action')
        amt_str = request.POST.get('amount') or "1"
        try:
            amount = max(1, int(amt_str))
        except ValueError:
            amount = 1
        delta = amount if action == 'inc' else -amount
        product.inventory = max(0, product.inventory + delta)
        product.save()
        messages.success(request, "Inventory updated.")
    return redirect('store_products', store_id=store.id)

@login_required
def adjust_price(request, store_id, product_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    product = get_object_or_404(Product, id=product_id, store=store)
    if request.method == 'POST':
        price_str = request.POST.get('price')
        try:
            new_price = Decimal(price_str)
        except Exception:
            messages.error(request, "Invalid price.")
            return redirect('store_products', store_id=store.id)
        if new_price < 0:
            new_price = Decimal('0')
        product.price = new_price
        product.save()
        messages.success(request, "Price updated.")
    return redirect('store_products', store_id=store.id)
@login_required
def add_product(request, store_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            try:
                tweet_product(product)
            except Exception:
                pass
            return redirect('store_products', store_id=store.id)
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form, 'store': store})

@login_required
def edit_product(request, store_id, product_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    product = get_object_or_404(Product, id=product_id, store=store)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('store_products', store_id=store.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/edit_product.html', {'form': form, 'store': store, 'product': product})

@login_required
def delete_product(request, store_id, product_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    product = get_object_or_404(Product, id=product_id, store=store)
    if request.method == 'POST':
        product.delete()
        return redirect('store_products', store_id=store.id)
    return render(request, 'store/delete_product.html', {'store': store, 'product': product})

# Buyer Views

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.filter(is_verified=True)
    purchased = False
    if request.user.is_authenticated:
        purchased = Order.objects.filter(user=request.user, items__product=product, is_paid=True).exists()
    return render(request, 'store/product_detail.html', {'product': product, 'reviews': reviews, 'purchased': purchased})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    qty_str = request.POST.get('quantity') or request.GET.get('quantity') or "1"
    try:
        quantity = max(1, int(qty_str))
    except ValueError:
        quantity = 1
    cart.add(product, quantity=quantity)
    messages.success(request, "Added to cart.")
    return redirect('product_list')

def view_cart(request):
    cart = Cart(request)
    return render(request, 'store/view_cart.html', {'cart': cart})

@login_required
def update_cart(request):
    if request.method != 'POST':
        return redirect('view_cart')
    cart = Cart(request)
    product_ids = list(cart.cart.keys())
    products = Product.objects.filter(id__in=product_ids)
    for product in products:
        field = f"quantity_{product.id}"
        qty = request.POST.get(field)
        if qty is not None:
            cart.update(product, qty)
    messages.success(request, "Cart updated.")
    return redirect('view_cart')

@login_required
def checkout(request):
    cart = Cart(request)
    if not cart.cart:
        messages.error(request, "Cart is empty.")
        return redirect('product_list')
    
    total_amount = cart.get_total_price()
    order = Order.objects.create(user=request.user, total_amount=total_amount, is_paid=True)
    
    invoice_lines = []
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['price']
        )
        item['product'].inventory = max(0, item['product'].inventory - item['quantity'])
        item['product'].save()
        invoice_lines.append(f"{item['product'].name} x {item['quantity']} - ${item['total_price']}")
    
    invoice_content = "Thank you for your order!\n\n" + "\n".join(invoice_lines) + f"\n\nTotal: ${total_amount}"
    
    send_mail(
        'Your Invoice',
        invoice_content,
        'noreply@eshop.com',
        [request.user.email],
        fail_silently=False,
    )
    
    cart.clear()
    messages.success(request, "Order placed successfully! Invoice sent to your email.")
    return redirect('product_list')

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    has_purchased = Order.objects.filter(
        user=request.user, 
        items__product=product,
        is_paid=True
    ).exists()
    if not has_purchased:
        messages.error(request, "Only verified purchasers can leave a review.")
        return redirect('product_detail', product_id=product.id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.is_verified = True
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'store/add_review.html', {'form': form, 'product': product})
