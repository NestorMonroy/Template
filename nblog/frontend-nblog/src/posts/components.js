import React, { useEffect, useState } from 'react'
import {loadPost} from '../lookup'

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
    const className = props.className ? props.className : 'btn btn-primary btn-small'
    return action.type === 'like' ? <button className={className}> {post.likes} Like</button> : null
}

export function Post(props) {
    const { post } = props
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
    return <div className={className}>
        <p>{post.id} -{post.content}</p>
        <div className='btn btn-group'>
            <ActionBtn post={post} action={{ type: "like" }} />

        </div>
    </div>

}