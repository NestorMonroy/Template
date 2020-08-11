import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import {
    Paper,
    Typography,
    Grid,
    IconButton
} from '@material-ui/core';
import EditIcon from '@material-ui/icons/Edit';
import DeleteForeverIcon from '@material-ui/icons/DeleteForever';

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
    pape2: {
        // padding: theme.spacing(1),
        marginLeft: theme.spacing(1),
        color: theme.palette.text.secondary,
        // display: 'grid',
        // gridTemplateColumns: '(1fr, auto, auto)',
        // gridGap: theme.spacing(3),
    },
    divider: {
        margin: theme.spacing(2, 0),
    },
    options: {
        lineHeight: '26px'
    },
    editButton: {
        // display: 'none',
        color: 'green',
        marginLeft: theme.spacing(1)
    },
    deleteButton: {
        // display: 'none',
        color: 'red',
        marginLeft: theme.spacing(1)
    },
}));


function PostList(props) {
    const { className, } = props;
    const classes = useStyles();
    const postClicked = post => evt => {
        props.postClicked(post)

    }
    const editClicked = post => {
        props.editClicked(post);
    }

    return (
        <Grid container spacing={3}>
            {props.posts && props.posts.map(post => {
                return (
                    <Grid item xs={12} key={post.id} >
                        <Paper>

                            <Typography
                                onClick={postClicked(post)}
                                component="h1"
                                variant="h3"
                            >
                                {post.content}

                                
                            </Typography>
                            <IconButton
                                className={classes.editButton}
                                onClick={() => editClicked(post)}

                            >
                                <EditIcon
                                />
                            </IconButton>
                            <IconButton className={classes.deleteButton}>
                                <DeleteForeverIcon />
                            </IconButton>

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