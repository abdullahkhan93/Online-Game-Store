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
from ..developer.forms import newGameForm
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden
from hashlib import md5


def library(request, message=None):
    if request.user.is_authenticated:
        user = request.user
        gameIDs = GamePurchase.objects.filter(userID=user, confirmed=True)
        gameIDs = list(map(lambda x: x.gameID.gameID, gameIDs))
        games = Game.objects.filter(gameID__in=gameIDs)
        return render(request, 'library.html', {'games': games})
    else:
        messages.add_message(request, messages.ERROR, 'You need to be logged in to access library page.')
        return redirect("login")


def gamestats(request, gameid):
    stats = GameStats.objects.filter(gameID=gameid, userID=userID).values()

    if len(stats) > 0:
        # converts datetime and other unserializable fields to str
        return HttpResponse(json.dumps(stats[0], default=str))
    else:
        return HttpResponse(
            'Stats not available for gameid={} & userid={}'.format(gameid)
        )


def refreshScoreboard(request, gameid):
    stats = GameStats.objects.filter(gameID=gameid)
    if len(stats) > 0:
        game = get_object_or_404(Game, gameID=gameid)
        scores = GameStats.objects.filter(gameID=game).order_by('-score')[:10]
        scoreList = map(lambda s: {'score': s.score, 'userID': s.userID}, scores)
        return render(request, 'scores.html', {'scores': scoreList})
    return HttpResponse('DASDASDASD') #TODO FIX


def gamepage(request, gameid):
    if request.user.is_authenticated:
        user = request.user
    
        games = GamePurchase.objects.filter(userID=user, confirmed=True)
        gameIDs = list(map(lambda x: x.gameID.gameID, games))
        if gameid in gameIDs:
            game = get_object_or_404(Game, gameID=gameid)
            scores = GameStats.objects.filter(gameID=game).order_by('-score')[:10]
            scoreList = map(lambda s: {'score': s.score, 'userID': s.userID}, scores)
            return render(request, 'gamepage.html', {'game': game, 'scores': scoreList })
        else:
            return HttpResponse('Please buy the game')
    else:
        return error403(request)


def save(request, gameid):
    if request.user.is_authenticated:
        userID = request.user.id
    
        if request.method == 'POST':
            rawData = request.POST['data']
            statsObject = get_object_or_404(GameStats, gameID=gameid, userID=userID)
            statsObject.gamestate = rawData
            statsObject.save()
            return HttpResponse('Success')    
    else:
        return error403(request)


def load(request, gameid):
    if request.user.is_authenticated:
        userID = request.user.id
    
        if request.method == 'GET':
            try:
                statsObject = get_object_or_404(GameStats, gameID=gameid, userID=userID)
                return HttpResponse(statsObject.gamestate)
            except:
                response = {'messageType': 'ERROR', 'info': 'Gamestate not found'}
                return HttpResponse(json.dumps(response))

    else:
        return error403(request)


def submitScore(request, gameid):
    if request.user.is_authenticated:
        userID = request.user.id
    
        if request.method == 'POST':
            rawData = request.POST['data']
            score = float(rawData)
            statsObject = get_object_or_404(GameStats, gameID=gameid, userID=userID)
            statsObject.score = score
            statsObject.date = time.strftime('%Y-%m-%d %H:%M')
            statsObject.save()
            return HttpResponse('Success')
    else:
        return error403(request)


def error404(request):
    return HttpResponseNotFound('Custom 404 Not Found')

def error500(request):
    return HttpResponseServerError('Custom 500 Server Error')

def error403(request):
    return HttpResponseForbidden('Custom 403 error')  