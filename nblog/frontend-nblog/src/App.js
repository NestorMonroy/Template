import React, { useEffect, useState } from 'react'
import logo from './logo.svg';
import './App.css';


function loadPost(callback) {
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

function Post(props){
  const {post} = props
  return <div className='col-10 mx-auto col-md-6'>
    <p>{post.content}</p>
  </div>

}
function App() {
  const [posts, setPosts] = useState([])


  useEffect(() => {
    const myCallback = (response, status) => {
      console.log(response, status)
      if (status === 200) {
        setPosts(response)
      } else{
        alert("Error")
      }
    }
    loadPost(myCallback)

  }, [])

  return (
    <div className="App">

      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <p>
          {posts.map((post, index) => {
            return <li>{post.content} </li>
          })}
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
