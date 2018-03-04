from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from django.template import loader
from django.contrib import messages
from django.shortcuts import get_list_or_404, get_object_or_404
import json
import time
from ..models import Game, GamePurchase, GameStats, Genre
import time
from hashlib import md5
from ..developer.forms import newGameForm
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden
from ..settings import PAYMENT_KEY, SID, SERVICE_URL
from social_django.models import UserSocialAuth


def shop(request):
    games = Game.objects.filter(visible=True)
    genres = Genre.objects.filter()
    if request.user.is_authenticated:
        purchases = GamePurchase.objects.filter(userID=request.user, confirmed=True)
        purchasedGames = list(map(lambda p: p.gameID.gameID, purchases))
        ownedGames = list(games.filter(pk__in=purchasedGames))
    else:
        ownedGames = []
    return render(request, 'shop.html', {'games': games, 'genres': genres, 'ownedGames': ownedGames})


def game(request, gameid):
    game = get_object_or_404(Game, gameID=gameid)
    owned = False
    if request.user.is_authenticated:
        purchase = GamePurchase.objects.filter(gameID=gameid, userID=request.user, confirmed=True)
        if len(purchase) > 0:
            owned = True
        else:
            owned = False
    return render(request, 'game.html', {'game': game, 'owned': owned})

def purchase(request, gameid):
    if request.user.is_authenticated:
        game = GamePurchase.objects.filter(userID=request.user, gameID=gameid, confirmed=True)
        if len(game) > 0:
            messages.add_message(request, messages.ERROR, 'You already have this game.')
            return redirect('shop')

        user = request.user
    
        game = get_object_or_404(Game, gameID=gameid)
        cost = game.price

        sellerID = game.developerID
        purchase = GamePurchase.objects.create(cost=cost,
                                               userID=user,
                                               gameID=game,
                                               sellerID=sellerID)
        pid = purchase.purchaseID
        purchase.save()
        stats = GameStats.objects.create(userID=user,
                                         gameID=game,
                                         score=0)
        stats.save()

        checksumStr = 'pid={}&sid={}&amount={}&token={}'.format(pid, SID, cost, PAYMENT_KEY)
        m = md5(checksumStr.encode("ascii"))
        checksum = m.hexdigest()

        return render(request, 'payment.html', {'game': gameid,
                                                'buyer': user,
                                                'price': cost,
                                                'pid': pid,
                                                'sid': SID,
                                                'checksum': checksum,
                                                'base_url': SERVICE_URL})
    else:
        messages.add_message(request, messages.ERROR, 'You need to be logged in to purchase the game.')
        return redirect("login")

def purchaseSuccess(request):
    params = request.GET
    checksumStr = 'pid={}&ref={}&result={}&token={}'.format(params['pid'],
                                                            params['ref'],
                                                            params['result'],
                                                            PAYMENT_KEY)
    m = md5(checksumStr.encode("ascii"))
    checksum = m.hexdigest()

    if checksum == params['checksum']:
        purchase = GamePurchase.objects.get(purchaseID=params['pid'])
        purchase.confirmed = True
        purchase.save()
        messages.add_message(request, messages.SUCCESS, 'Game purchased!')
        return redirect('library')
    else:
        get_object_or_404(GamePurchase, purchaseID=params['pid']).delete()
        messages.add_message(request, messages.ERROR, 'Error in payment')
        return redirect('library')

def purchaseFail(request):
    messages.add_message(request, messages.ERROR, 'Error in purchasing')
    return redirect('library')