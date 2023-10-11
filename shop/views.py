from django.shortcuts import render, redirect
from shop import models
from .forms import Itemform
from .models import Item, Order
from django.contrib import messages
import uuid
from django.contrib.auth.models import User, auth


# Create your views here.

def item_show(request, item_uuid):
    item_to_send = Item.objects.filter(item_id=item_uuid)
    if item_to_send.exists():
        return render(request, "item.html", {'title': item_to_send[0].item_name, 'item': item_to_send[0]})
    else:
        messages.info(request, "Item does not exists!")
        return redirect("/")


def my_order(request):
    if request.user.is_authenticated:
        orders = models.Order.objects.filter(order_item_from=request.user.username)
        return render(request, "orders.html", {'orders': orders, 'title': 'Orders'})
    else:
        messages.info(request, "Seems like you are not logged in!")
        return redirect("/") 


# def checkout(request, item_uuid):
#    if request.user.is_authenticated:
#        return render(request, "checkout.html")
#    else:
#        messages.info(request, "Seems like you are not logged in! Please log in to place orders. Register if you dont have an account!")
#        return redirect("/")


def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("/")
            else:
                messages.info(request, "Invalid Credentials")
                return redirect('/login')
        else:
            return render(request, "login.html", {"title": "Login"})
    else:
        messages.info(request, "Seems like your are already logged in!")
        return redirect("/")


def update_items(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = Itemform(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.added_by = request.user.username
                obj.item_id = uuid.uuid4()
                form.save()
            else:
                messages.info(request, "Data is not valid!")
                return redirect("/add")
            return redirect("/")
        my_form = Itemform()
        return render(request, "add.html", context={"my_form": my_form, "title": "Update Items"})
    else:
        messages.info(request, "Seems like your are not logged in! Please login or register a new account!")
        return redirect("/")


def manage_items(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            item_to_delete = request.POST
            key_list = list(item_to_delete.keys())
            other_items = False
            for i_id in key_list:
                i = Item.objects.filter(item_id=i_id)
                if item_to_delete[i_id] == "on" and len(i) != 0:
                    if request.user.username == i[0].added_by:
                        i.delete()
                    else:
                        other_items = True
            if other_items:
                messages.info(request, "All selected items are deleted (except other's item)!")
        data = Item.objects.filter(added_by=request.user.username)
        return render(request, "manage.html", {'data': data, 'title': 'Manage'})
    else:
        messages.info(request, "Seems like your are not logged in! Please login or register a new account!")
        return redirect("/")


def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            firstname = request.POST["firstname"]
            lastname = request.POST["lastname"]
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            confirmpsw = request.POST["confirmpsw"]

            if firstname and lastname and username and email and password and confirmpsw != "":
                if confirmpsw == password:
                    if not User.objects.filter(username=username).exists():
                        if not User.objects.filter(email=email).exists():
                            user_inst = User.objects.create_user(first_name=firstname, last_name=lastname,
                                                                 username=username,
                                                                 email=email, password=password)
                            user_inst.save()
                            messages.info(request, "Account Registered! Please log in to continue")
                            return redirect("/")
                        else:
                            messages.info(request, "Email already registered!")
                            return redirect("/register")
                    else:
                        messages.info(request, "Username already exists!")
                        return redirect("/register")
                else:
                    messages.info(request, "Password not matching!")
                    return redirect("/register")
            else:
                messages.info(request, "Fields are empty!")
                return redirect("/register")
        return render(request, "register.html", {"title": "Register"})
    else:
        messages.info(request, "You are already logged in!")
        return redirect("/")


def buy_items(request):
    items = models.Item.objects.all()
    return render(request, "shop.html", {"title": "Buy", "items": items})


def change(request):
    return redirect("/manage")


def change_item_details(request, item_uuid):
    if request.user.is_authenticated:
        try:
            form = Item.objects.get(item_id=item_uuid)
        except:
            messages.info(request, "Item does not exists!")
            return redirect("/manage")

        if form.added_by != request.user.username:
            messages.info(request, "Heh! You cant access someone else's item")
            return redirect("/manage")

        if request.method == "POST":
            if form.added_by != request.user.username:
                messages.info(request, "Item you are trying to change does not belongs to you")
                return redirect("/manage")
            inst = Itemform(request.POST, request.FILES, instance=form)
            for i in request.POST:
                if i == "" or None:
                    messages.info(request, "Please fill all details")
                    return redirect("/change" + item_uuid)

            if inst.is_valid():
                new_save = inst.save(commit=False)
                new_save.added_by = request.user.username
                new_save.save()
                messages.info(request, "Successfully Updated!")
                return  redirect("/manage")
            else:
                messages.info(request, "Data is invalid!")
                return render(request, "change.html",
                              {"title": "Change",
                               "item_uuid": item_uuid,
                               "image": form.item_image,
                               "my_form": Itemform(initial={"item_name": form.item_name,
                                                            "item_description": form.item_description,
                                                            "item_price": form.item_price,
                                                            "item_price_currency": form.item_price_currency
                                                            }
                                                   )
                               }
                              )
        else:
            return render(request, "change.html",
                          {"title": "Change",
                           "item_uuid": item_uuid,
                           "image": form.item_image ,
                           "my_form": Itemform(initial={"item_name": form.item_name,
                                                        "item_description": form.item_description,
                                                        "item_price": form.item_price,
                                                        "item_price_currency": form.item_price_currency
                                                        }
                                               )
                           }
                          )
    else:
        messages.info(request, "Seems like your are not logged in! Please login or register a new account!")
        return redirect("/")


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.info(request, "Successfully Logged Out!")
        return redirect('/')
    else:
        messages.info(request, "Seems like your are not logged in! Please login or register a new account!")
        return redirect("/")


def purchase(request):
    if request.user.is_authenticated:
        pass
    else:
        messages.info(request, "Seems like your are not logged in! Please login or register a new account!")
        return redirect("/")