

export function loadPost(callback) {
    const xhr = new XMLHttpRequest()
    const method = 'GET'
    const url = 'http://localhost:8000/api/post/posts/'
    const responseTYpe = 'json'

    xhr.responseType = responseTYpe
    xhr.open(method, url)
    xhr.onload = function () {
        callback(xhr.response, xhr.status)
    }
    xhr.onerror = function (e) {
        console.log(e)
        callback({ "message": "Error" }, 400)
    }
    xhr.send()
}

