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

function LikeBtn(props) {
  const {post} =props
  const className = props.className ? props.className: 'btn btn-primary btn-small'
  return <button className={className}> {post.likes} Like</button>
}

function Post(props){
  const {post} = props
  const className = props.className ? props.className: 'col-10 mx-auto col-md-6'
  return <div className={className}>
    <p>{post.id} -{post.content}</p>
    <div className='btn btn-group'>
      <LikeBtn post={post} />

    </div>
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
        <div>
          {posts.map((item, index) => {
            return <Post post={item} className='my-5 py-5 border border-white' key={`${index}-{item.id}`} />
          })}
        </div>
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
