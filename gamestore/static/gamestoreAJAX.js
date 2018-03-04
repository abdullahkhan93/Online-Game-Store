const _getCRFS = () => {
    let obj = {};
    let str = document.cookie;        
    str = str.split(', ');
    for (let i = 0; i < str.length; i++) {
        let tmp = str[i].split('=');
        obj[tmp[0]] = tmp[1];
    }
    return obj['csrftoken'];
}

const gamestoreAJAX = {
    get: (url) => $.ajax({
        type: 'GET',
        url: url,
        beforeSend: (request) => {
            request.setRequestHeader("Authority", _getCRFS());
        },
        contentType: 'application/x-www-form-urlencoded'
    }),
    post: (url, data) => $.ajax({
        type: 'POST',
        url: url,
        dataType: 'text html',
        data: data,
        beforeSend: (request) => {
            request.setRequestHeader('X-CSRFToken', _getCRFS());
        },
    })
};