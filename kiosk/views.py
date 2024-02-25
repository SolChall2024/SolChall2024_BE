import os
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.http import JsonResponse

from .forms import RegisterForm, LoginForm, MenuForm, OptionForm, OptionContentForm
from .models import Store, Menu, Option, OptionContent, Cart, Order, Category
from django.db.models import Sum
from google.cloud import speech_v1
from google.oauth2 import service_account
from django.http import JsonResponse
from django.conf import settings
from random import choice
from django.http import JsonResponse
import json



def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 아이디 중복 확인
            username = form.cleaned_data['username']
            if Store.objects.filter(username=username).exists():
                messages.error(request, '이미 사용 중인 아이디입니다.')
            else:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password2'])  # 비밀번호 설정 부분 수정
                user.save()
                # 회원가입 후 자동으로 로그인
                login(request, user)
                print("회원가입이 성공적으로 완료되었습니다.")
                return redirect('/login')  # 로그인 후 메뉴 페이지로 이동
    else:
        form = RegisterForm()
    return render(request, 'kiosk/sign_up.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['id']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/menu')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'kiosk/login.html', {'form': form})


def user_logout(request):
    logout(request)  # 현재 사용자 세션 종료
    return redirect('/login')



# Create your views here.
def landing(request):
    return render(request, 'kiosk/landing.html', {})

def search_or_browse(request):
    return render(request, 'kiosk/search_or_browse.html', {})

def search(request):
    return render(request, 'kiosk/search.html', {})

def browse(request):
    categories = Category.objects.all()
    menus = Menu.objects.all()

    return render(
    request,
    'kiosk/browse.html',
    {
        'categories' : categories,
        'menus' : menus
    }
)

def menu_options(request, menu_id):
    # menu = Menu.objects.get(pk=menu_id)
    #
    # options_ids = menu.optionid.all()
    #
    # options = Option.objects.filter(pk__in=option_ids)
    #
    # #options = menu.option_set.all()
    # return render(request, 'kiosk/option.html', {'menu': menu})

    # Retrieve the menu item based on the menu ID
    menu = Menu.objects.get(pk=menu_id)
    # Retrieve the option IDs associated with the menu item
    option_ids = menu.optionId.all()
    # Retrieve the options based on the option IDs
    options = Option.objects.filter(pk__in=option_ids)

    return render(request, 'kiosk/option.html', {'menu': menu, 'options': options})


def convert_speech_to_text(request):

    if request.method == 'POST':
        # 클라이언트로부터 받은 음성 텍스트
        audio_text = request.POST.get('audio_text')

        # JSON 파일의 경로 설정
        #json_file_path = os.path.join(settings.BASE_DIR, 'kiosk', 'solutionproject-414810-6aa45c89e5cc.json')
        credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

        # Google STT API 인증 정보
        #credentials = service_account.Credentials.from_service_account_file(json_file_path)
        credentials = service_account.Credentials.from_service_account_file(credentials_path)


        # Google STT 클라이언트 생성
        client = speech_v1.SpeechClient(credentials=credentials)

        # 음성 텍스트를 변환합니다.
        response = client.recognize({
            'config': {
                'encoding': 'LINEAR16',
                'sample_rate_hertz': 44100,
                'language_code': 'ko-KR',
            },
            'audio': {
                'content': audio_text,
            }
        })

        # 변환된 텍스트를 추출합니다.
        recognized_text = response.results[0].alternatives[0].transcript

        recognized_text = recognized_text.rstrip('.')

        return JsonResponse({'text': recognized_text})

def get_menu_id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transcription = data.get('transcription', '').replace(" ", "")
        print(f'Transcription received: {transcription}')
        # Search for the Menu object based on the recognized text
        try:
            menus = Menu.objects.filter(name=transcription)
            if menus.exists():
                menu_ids = menus.first().pk
                print(menu_ids)
                return JsonResponse({'menu_ids': menu_ids})
            else:
                return JsonResponse({'error': 'Menu not found'}, status=404)
        except Menu.DoesNotExist:
            return JsonResponse({'error': 'Menu not found'}, status=404)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)


def cart(request):
    carts = Cart.objects.all()

    total_quantity = len(carts)
    total_price = Cart.objects.aggregate(total_price=Sum('price'))['total_price']

    return render(
    request,
    'kiosk/cart.html',
    {
        'carts': carts,
        'total_quantity': total_quantity,
        'total_price' : total_price
    }
)

def pay(request):
    carts = Cart.objects.all()
    total_price = 0

    for c in carts:
        total_price += c.price

    return render(
    request,
    'kiosk/pay.html',
    {
        'total_price': total_price
    }
)

def success(request):
    latest_order = Order.objects.all().order_by('-pk').first()

    return render(
    request,
    'kiosk/order_success.html',
    {
        'latest_order' : latest_order
    }
)


@csrf_exempt
def delete(request):
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        card = get_object_or_404(Cart, cartId=card_id)
        card.delete()


        carts = Cart.objects.all()
        total_quantity = len(carts)
        total_price = Cart.objects.aggregate(total_price=Sum('price'))['total_price']

        data_and_message = {
            'total_quantity' : total_quantity,
            'total_price' : total_price,
            'message' : '카트 삭제'
        }

        # 성공적으로 삭제되었다는 응답을 반환
        return JsonResponse(data_and_message)

    # POST 요청이 아닌 경우 에러 응답
    return JsonResponse({'error': '올바르지 않은 요청입니다.'}, status=400)



def menu(request):
    if request.user.is_authenticated:
        store_name = request.user.last_name  # 로그인한 사용자의 가게 이름을 가져옵니다.

        # 현재 사용자의 가게에 해당하는 카테고리를 가져옵니다.
        categories = Category.objects.filter(menu__storeId=request.user.id).distinct()

        # 요청 쿼리 매개변수에서 선택한 카테고리를 가져옵니다.
        selected_category_id = request.GET.get('category')

        # 선택한 카테고리가 없거나 선택한 카테고리가 사용자의 가게에 속하지 않는 경우, 첫 번째 카테고리를 선택합니다.
        if not selected_category_id or not categories.filter(categoryId=selected_category_id).exists():
            selected_category = categories.first()
        else:
            selected_category = categories.get(categoryId=selected_category_id)

        # 현재 사용자의 가게에 대해 카테고리별로 메뉴를 가져옵니다.
        menu_by_category = {}
        for category in categories:
            drinks = Menu.objects.filter(storeId=request.user.id, categoryId=category)
            menu_by_category[category] = drinks

        context = {
            'store_name': store_name,
            'menu_by_category': menu_by_category,
            'selected_category': selected_category,
            'categories': categories,  # 템플릿에서 카테고리 목록을 사용할 수 있도록 추가합니다.
        }
    else:
        context = {}
    return render(request, 'kiosk/menu.html', context)


@login_required
def add_menu(request):
    categories = Category.objects.all()
    options = Option.objects.all()  # 모든 옵션 목록을 가져옴

    if request.method == 'POST':
        menu_form = MenuForm(request.POST, request.FILES)
        option_content_form = OptionContentForm(request.POST)

        if menu_form.is_valid() and option_content_form.is_valid():
            menu = menu_form.save(commit=False)
            menu.storeId_id = request.user.id

            category_id = request.POST.get('category')
            if category_id and category_id != "add_new_category":
                menu.categoryId_id = category_id
            else:
                new_category_name = request.POST.get('new_category')
                if new_category_name:
                    category = Category.objects.create(name=new_category_name)
                    menu.categoryId = category

            menu.save()

            option_content = option_content_form.save(commit=False)
            option_content.save()

            # 사용자가 선택한 옵션을 가져옴
            selected_option_id = request.POST.get('option')
            if selected_option_id and selected_option_id != "add_new_option":
                # 옵션의 ID를 정수형으로 변환하여 가져오기
                selected_option_id = int(selected_option_id)
                selected_option = Option.objects.get(pk=selected_option_id)
                selected_option.menuId.add(menu)  # 해당 옵션과 메뉴를 연결함

            # 새로운 옵션을 추가하는 경우
            else:
                new_option_name = request.POST.get('new_option')
                if new_option_name:
                    new_option = Option.objects.create(option=new_option_name, price=0)
                    new_option.menuId.add(menu)

            return redirect('/menu')

    else:
        menu_form = MenuForm()
        option_content_form = OptionContentForm()

    return render(request, 'kiosk/add_menu.html',
                  {'menu_form': menu_form, 'option_content_form': option_content_form,
                   'categories': categories, 'options': options})




def add_to_cart(request):
    if request.method == 'POST':
        menu_id = request.POST.get('menu_id')
        selected_contents = request.POST.get('selected_content')
        quantity = int(request.POST.get('quantity'))
        price = int(request.POST.get('price'))

        # 메뉴 객체 가져오기
        menu = Menu.objects.get(pk=menu_id)

        # 장바구니에 추가
        for i in range(quantity):
            Cart.objects.create(
                menuId=menu,
                price=price,
                options=selected_contents,
            )

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})