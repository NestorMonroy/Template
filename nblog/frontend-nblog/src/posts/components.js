import React, { useEffect, useState } from 'react'
import { loadPost } from '../lookup'

export function PostsComponent(props) {
    const textAreaRef = React.createRef()
    const handleSubmit = (event) => {
        event.preventDefault()
        // console.log(event)
        // console.log(textAreaRef.current.value)
        const newVal = textAreaRef.current.value
        console.log(newVal)
        
        textAreaRef.current.value = ''

    }

    return <div className={props.className}>
        <div className='col-12 mb-3'>
            <form onSubmit={handleSubmit}>
                <textarea  ref={textAreaRef} required={true} className='form-control'>

                </textarea>
                <button type='submit' className='btn btn-primary my-3' > Post</button>
            </form>
        </div>
    <PostsList/>
    </div>
}

export function PostsList(props) {
    const [posts, setPosts] = useState([])

    useEffect(() => {
        const myCallback = (response, status) => {
            console.log(response, status)
            if (status === 200) {
                setPosts(response)
            } else {
                alert("Error")
            }
        }
        loadPost(myCallback)

    }, [])
    return posts.map((item, index) => {
        return <Post post={item} className='my-5 py-5 border border-white' key={`${index}-{item.id}`} />
    })

}

export function ActionBtn(props) {
    const { post, action } = props
    const [likes, setLikes] = useState(post.likes ? post.likes : 0)
    const [userLike, setUserLike] = useState(false)

    const className = props.className ? props.className : 'btn btn-primary btn-small'
    const acctionDisplay = action.display ? action.display : 'Action'
    const handleClick = (event) => {
        event.preventDefault()
        if (action.type === 'like') {
            if (userLike === true) {
                setLikes(likes - 1)
                setUserLike(false)
            } else {
                setLikes(likes + 1)
                setUserLike(true)
            }
            // console.log(post.likes+1)

        }
    }
    const display = action.type === 'like' ? `${likes} ${acctionDisplay}` : acctionDisplay

    return <button className={className} onClick={handleClick}  > {display} </button>
}

export function Post(props) {
    const { post } = props
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
    return <div className={className}>
        <p>{post.id} -{post.content}</p>
        <div className='btn btn-group'>
            <ActionBtn post={post} action={{ type: "like", display: "Like" }} />
            <ActionBtn post={post} action={{ type: "unlike", display: "Unlike" }} />
            <ActionBtn post={post} action={{ type: "repost" }} />

        </div>
    </div>

}