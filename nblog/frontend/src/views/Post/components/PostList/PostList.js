import React from 'react';
import { LInk } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import {
    Button,
    Paper,
    Typography,
    Grid,
    IconButton,
    Container,
    Card
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
    blue: {
        color: 'blue'
    }
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
        <Paper className={classes.paper}>
            {props.posts && props.posts.map(post => {
                return (
                    <Grid container justify="center" wrap="nowrap" spacing={2} key={post.id}>
                        <Grid item>
                            <Typography component="h1" variant="h3">
                                {post.content}
                            </Typography>
                        </Grid>
                        <Grid item>
                            <IconButton
                                className={classes.editButton}

                            >
                                <EditIcon
                                />
                            </IconButton>
                        </Grid>
                        <Grid item>
                            <IconButton
                                className={classes.deleteButton}
                            >
                                <DeleteForeverIcon
                                />
                            </IconButton>
                        </Grid>
                    </Grid>
                                    )
                                })}
        </Paper>
    )
}
export default PostList;