import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import {
    Paper,
    Typography,
    Grid
} from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
    root: {},
    content: {
        display: 'flex',
        alignItems: 'center'
    },
    input: {
        width: '100%'
    },
    fileInput: {
        display: 'none'
    },
    container: {
        display: 'grid',
        gridTemplateColumns: 'repeat(12, 1fr)',
        gridGap: theme.spacing(3),
    },
    paper: {
        padding: theme.spacing(1),
        textAlign: 'center',
        color: theme.palette.text.secondary,
        whiteSpace: 'nowrap',
        marginBottom: theme.spacing(1),
    },
    divider: {
        margin: theme.spacing(2, 0),
    },
    options: {
        lineHeight: '26px'
    },
}));


function PostList(props) {
    const { className, } = props;
    const classes = useStyles();
    const postClicked = post => evt => {
        props.postClicked(post)

    }

    return (
        <Grid container spacing={3}>
            {props.posts && props.posts.map(post => {
                return (
                    <Grid item xs={12} key={post.id} >
                        <Paper className={classes.paper}>

                            <Typography
                                onClick={postClicked(post)}
                                component="h1"
                                variant="h3"
                            >
                                {post.content}
                            </Typography>
                            {/* <Typography
                                className={classes.options}
                                variant="subtitle2"
                            >
                            {props.post && props.post.content}
                            </Typography> */}
                        </Paper>
                    </Grid>
                )
            })}
        </Grid>
    )

}
export default PostList;