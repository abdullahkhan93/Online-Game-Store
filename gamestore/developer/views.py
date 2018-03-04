from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from django.contrib import messages
from django.shortcuts import get_list_or_404, get_object_or_404
import json
import time
from ..models import Game, GamePurchase, GameStats, Genre, UserAttributes
from .forms import newGameForm
from django.contrib.auth.models import User
import datetime
import json

# Create your views here.

def developerpage(request):
    if request.user.is_authenticated:
        attributes = UserAttributes.objects.filter(userID=request.user)
        if len(attributes) > 0:
            if attributes[0].isDeveloper == True:
                games = Game.objects.filter(developerID=request.user)
                return render(request, 'addNewGame.html', {'games': games, 'form': newGameForm, 'devpageTitle': 'Add a new game'})
    messages.add_message(request, messages.ERROR, 'You need to be a developer to access developer page.')
    return redirect('shop')


def modifygamepage(request, gameid):
    if request.user.is_authenticated:
        games = Game.objects.filter(developerID=request.user)
        game = Game.objects.filter(developerID=request.user, gameID=gameid)

        if len(game) > 0:
            game = game.get()
            form = newGameForm(request.POST or None, instance=game)
            if form.is_valid():
                form.save()
                return redirect('developer')

            return render(request, 'modifyGame.html', {'games': games, 'form': form, 'devpageTitle': game.name, 'game': game})
        return HttpResponse('you dont have access to this page') #TODO redirect or something
    else:
        messages.add_message(request, messages.ERROR, 'You need to be logged in to access developer page.')
        return redirect('login')

# todo: combine with dev page view
def addGame(request):
    if request.user.is_authenticated:
        userID = request.user.id
    
        if request.method == 'POST':
            form = newGameForm(request.POST, request.FILES)
            if form.is_valid:
                try:
                    game = form.save(commit=False)
                    game.developerID = get_object_or_404(User, id=userID)
                    game.save()
                    purchase = GamePurchase.objects.create(cost=0,
                                                           userID=request.user,
                                                           gameID=game,
                                                           sellerID=request.user,
                                                           confirmed=True)
                    purchase.save()
                    stats = GameStats.objects.create(userID=request.user,
                                                     gameID=game,
                                                     score=0)
                    stats.save()
                    messages.add_message(request, messages.SUCCESS, 'Game created')
                    return redirect('developer')
                except:
                    pass

    messages.add_message(request, messages.ERROR, 'Invalid form')
    return redirect('developer')


def getSalesStatistics(request, gameid):
    if request.user.is_authenticated:
        userID = request.user.id
        games = Game.objects.filter(developerID=request.user, gameID=gameid)

        if len(games) > 0:
            game = games[0]
            purchases = GamePurchase.objects.filter(gameID=game)
            purchasesList = [{'date': p.date.strftime("%Y-%m-%d"), 'cost': p.cost} for p in purchases]
            totalSales = len(purchasesList)
            totalRevenue = sum(map(lambda x: x['cost'], purchasesList))

            combinedList = dict()
            for p in purchasesList:
                if p['date'] not in combinedList:
                    combinedList[p['date']] = (p['cost'], 1)
                else:
                    item = combinedList[p['date']]
                    combinedList[p['date']] = (item[0]+p['cost'], item[1]+1)
                
            finalList = [{'date': p[0], 'revenue': p[1][0], 'sales': p[1][1]} for p in combinedList.items()]

            response = {
                'status': 'success',
                'data': {
                    'totals': {
                        'totalSales': totalSales,
                        'totalRevenue': totalRevenue
                    },
                    'sales': finalList
                }
            }
            return HttpResponse(json.dumps(response))

    return HttpResponse('{ status: "error", data: "you are not authorized"}')

        
def becomeDev(request):
    if request.user.is_authenticated:
        userID = request.user.id
        attributes = UserAttributes.objects.get(userID=request.user)
        if attributes.isDeveloper == False:
            attributes.isDeveloper = True
            attributes.save()
            messages.add_message(request, messages.SUCCESS, 'You are now a developer.')
            return redirect('developer')
        else:
            messages.add_message(request, messages.ERROR, 'You are a developer already.')
            return redirect('developer')

    messages.add_message(request, messages.ERROR, 'Error')
    return redirect('shop')