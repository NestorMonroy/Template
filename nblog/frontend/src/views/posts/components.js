import React, { useEffect, useState } from 'react';
import makeStyles from '@material-ui/core/styles/makeStyles';
import StarRateIcon from '@material-ui/icons/StarRate';
import EditIcon from '@material-ui/icons/Edit';
import { useDispatch } from 'react-redux';
import MoreIcon from '@material-ui/icons';
import {
    Avatar,
    Button,
    Card,
    CardContent,
    CardHeader,
    Divider,
    Grid,
    IconButton,
    ButtonBase,
    Link,
    Tooltip,
    Typography,
    colors,
    Paper
} from '@material-ui/core';
// import { loadPost } from '../lookup'

const useStyles = makeStyles((theme) => ({
    root: {
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: theme.spacing(6, 2)
    },
    paper: {
        padding: theme.spacing(2),
        margin: 'auto',
        maxWidth: 500
    },
    image: {
        width: 128,
        height: 128
    },
    img: {
        margin: 'auto',
        display: 'block',
        maxWidth: '100%',
        maxHeight: '100%'
    },
    cartButton: {
        marginLeft: theme.spacing(1)
    },
}));

export function PostsComponent(props) {
    const textAreaRef = React.createRef();
    const [newPosts, setNewPosts] = useState([]);
    const handleSubmit = (event) => {
        event.preventDefault();
        const newVal = textAreaRef.current.value;
        let tempNewPosts = [...newPosts];
        tempNewPosts.unshift({
            content: newVal,
            likes: 0,
            id: 124
        });
        setNewPosts(tempNewPosts);
        textAreaRef.current.value = '';
    };

    return (
        <div className={props.className}>
            <div className="col-12 mb-3">
                <form onSubmit={handleSubmit}>
                    <textarea ref={textAreaRef} required={true} className="form-control" />
                    <button type="submit" className="btn btn-primary my-3">
                        {' '}
						Post
					</button>
                </form>
            </div>
            <PostsList newPosts={newPosts} />
        </div>
    );
}

export function PostsList(props) {
    const classes = useStyles();
    const postClicked = (post) => (event) => {
        props.postClicked(post);
    };

    return (
        <div className={classes.root}>
            <Paper className={classes.paper}>
                <Grid container spacing={2}>
                    <Grid item xs={12} sm container>
                        <Grid item xs container direction="column" spacing={2}>
                            <Grid item xs>
                                {props.posts &&
                                    props.posts.map((post) => {
                                        return (
                                            <Typography key={post.id} variant="subtitle1">
                                                <Typography onClick={postClicked(post)}>{post.content}</Typography>
                                            </Typography>
                                        );
                                    })}
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Paper>
        </div>
    );
}

export function PostsDetails(props) {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <Paper className={classes.paper}>
                <Grid container spacing={2}>
                    <Grid item xs={12} sm container>
                        <Grid item xs container direction="column" spacing={2}>
                            <Grid item xs>
                                {props.post ? (
                                    <Typography variant="subtitle1">{props.post.content}
                                        <IconButton
                                            className={classes.cartButton}
                                            size="small"
                                        >
                                            <StarRateIcon  />
                                        </IconButton>
                                    </Typography>
                                ) : null}

                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Paper>
        </div>
    );
}

// export function PostsList(props) {
//     const [postsInit, setPostsInit] = useState([])
//     const [posts, setPosts] = useState([])

//     useEffect(() => {
//         const final = [...props.newPosts].concat(postsInit)
//         if (final.length !== posts.length) {
//             setPosts(final)
//         }
//     }, [props.newPosts, posts, postsInit])

//     useEffect(() => {
//         fetch("http://127.0.0.1:8000/api/post/posts", {
//             method: 'GET',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'Authorization': 'Token 76b7c13ce9866bace4f25f6018f74a137f0852de'
//             }
//         })
//             .then(resp => resp.json())
//             .then(resp => setPosts(resp))
//             .catch(error => console.log(error))
//     }, [postsInit])

//     // useEffect(() => {
//     //     const myCallback = (response, status) => {
//     //         // console.log(response, status)
//     //         if (status === 200) {
//     //             setPostsInit(response)
//     //         } else {
//     //             alert("Error")
//     //         }
//     //     }
//     //     loadPost(myCallback)
//     // }, [postsInit])

//     return posts.map((item, index) => {
//         return <Post post={item} className='my-5 py-5 border border-white' key={`${index}-{item.id}`} />
//     })

// }

export function ActionBtn(props) {
    const { post, action } = props;
    const [likes, setLikes] = useState(post.likes ? post.likes : 0);
    const [userLike, setUserLike] = useState(false);

    const className = props.className ? props.className : 'btn btn-primary btn-small';
    const acctionDisplay = action.display ? action.display : 'Action';
    const handleClick = (event) => {
        event.preventDefault();
        if (action.type === 'like') {
            if (userLike === true) {
                setLikes(likes - 1);
                setUserLike(false);
            } else {
                setLikes(likes + 1);
                setUserLike(true);
            }
            // console.log(post.likes+1)
        }
    };
    const display = action.type === 'like' ? `${likes} ${acctionDisplay}` : acctionDisplay;

    return (
        <button className={className} onClick={handleClick}>
            {' '}
            {display}{' '}
        </button>
    );
}

export function Post(props) {
    const { post } = props;
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6';
    return (
        <div className={className}>
            <p>
                {post.id} -{post.content}
            </p>
            <div className="btn btn-group">
                <ActionBtn post={post} action={{ type: 'like', display: 'Like' }} />
                <ActionBtn post={post} action={{ type: 'unlike', display: 'Unlike' }} />
                <ActionBtn post={post} action={{ type: 'repost' }} />
            </div>
        </div>
    );
}
