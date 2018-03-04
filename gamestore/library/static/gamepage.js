$( document ).ready(() => {
    window.addEventListener('message', receiveMessage, false);

    function receiveMessage(event) {
        // console.log('message received');
        // console.log(event.data);
        processMessage(event);
    }

    function processMessage(event) {
        data = event.data;
        switch (data.messageType) {
            case 'SETTING':
                gameFrame = document.getElementById('game');
                $('#game').css({
                    'height': data.options.height,
                    'width': data.options.width
                });
                break;
            case 'SAVE':
                gamestoreAJAX
                    .post('save', 'data='+JSON.stringify(data))
                    .done(() => console.log('saved'));
                break;
            case 'LOAD_REQUEST':
                gamestoreAJAX
                    .get('load')
                    .done(res => {
                        loadState(res, event);
                    });
                break;
            case 'SCORE':
                gamestoreAJAX
                    .post('score', 'data='+JSON.stringify(data.score))
                    .done(() => $('#highscores').load("gethighscore"));
        }
    }

    function loadState(text, event) {
        let serverMessage = JSON.parse(text)
        if (serverMessage.messageType == 'SAVE') {
            let response = {
                messageType: 'LOAD',
                gameState: serverMessage.gameState
            };
            event.source.postMessage(response, event.origin);
        } else if (serverMessage.messageType == 'ERROR') {
            event.source.postMessage(serverMessage, event.origin);
        }
    }
})