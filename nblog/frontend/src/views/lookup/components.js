import React, { Fragment, useState, useEffect } from "react";


// export function loadPost(callback) {
//     const xhr = new XMLHttpRequest()
//     const method = 'GET'
//     const url = 'http://localhost:8000/api/post/posts/'
//     const responseTYpe = 'json'

//     xhr.responseType = responseTYpe
//     xhr.open(method, url)
//     xhr.onload = function () {
//         callback(xhr.response, xhr.status)
//     }
//     xhr.onerror = function (e) {
//         console.log(e)
//         callback({ "message": "Error" }, 400)
//     }
//     xhr.send()
// }




// export function loadPost(callback) {
//     const [posts, setPost] = useState([]);

//     useEffect(() => {
//         fetch("http://127.0.0.1:8000/api/post/posts", {
//             method: 'GET',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'Authorization': 'Token 76b7c13ce9866bace4f25f6018f74a137f0852de'
//             }
//         })
//             .then(resp => resp.json())
//             .then(resp => setPost(resp))
//             .catch(error => console.log(error))
//     }, [callback])
// }


