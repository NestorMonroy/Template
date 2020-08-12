import React, { useState, useRef } from 'react';
import clsx from 'clsx';

import {
    Container,
    Grid,
    Card,
    CardActions,
    CardContent,
    Divider,
    Typography,

    TextareaAutosize,
    Tooltip,
    Paper,
    Input,
    IconButton,

} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import SendIcon from '@material-ui/icons/Send';
import AddPhotoIcon from '@material-ui/icons/AddPhotoAlternate';
import AttachFileIcon from '@material-ui/icons/AttachFile';
// import {postService} from '../../../'
import {postService} from "src/services/postService";
const useStyles = makeStyles((theme) => ({
    root: {},
    content: {
        display: 'flex',
        alignItems: 'center'
    },
    cardHeader: {

    },
    paper: {
        flexGrow: 1,
        padding: theme.spacing(0.5, 2)
    },

}));


function PostForm(props) {
    const classes = useStyles();
    const { className, } = props;
    const [value, setValue] = useState('');
    // const session = useSelector((state) => state.session);

    const [content, setContent] = useState(props.post.content)


    const fileInputRef = useRef(null);

    const handleChange = (event) => {
        event.persist();
        setValue(event.target.value);
    };


    const handleAttach = () => {
        fileInputRef.current.click();
    };

    
    const updateClicked = () => {
        // console.log('here')
        postService.updatePost(props.post.id, {content})
        .then(resp => console.log(resp))
        console.log(props.post.id)

    };


    return (
        <Container maxWidth="md" component="main">
            <Grid container spacing={2} alignItems="flex-end">
                <Grid item xs={12}>

                    <Card
                        className={classes.root}
                    // className={clsx(classes.root, className)}
                    >
                        <CardContent className={classes.content}>
                            {props.post ? (
                                <React.Fragment>

                                    <Paper
                                        className={classes.paper}
                                        elevation={1}
                                    >

                                        <TextareaAutosize
                                            rowsMax={4}
                                            aria-label="maximum height"
                                            className={classes.input}
                                            id="content"
                                            value={content}
                                            onChange={evt=> setContent(evt.target.value)}
                                            //defaultValue={props.post.content}
                                        />

                                        {/* <Input
                                            id={props.content}
                                            className={classes.input}
                                            disableUnderline
         

                                        /> */}


                                    </Paper>
                                    <Tooltip title="Send">
                                        <IconButton onClick={updateClicked} color={value.length > 0 ? 'primary' : 'default'}>
                                            <SendIcon />
                                        </IconButton>
                                    </Tooltip>


                                </React.Fragment>
                            ) : null}

                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Container>

    )
}

export default PostForm;



{/* <Card>
<CardContent>
    <Typography paragraph>
        <TextareaAutosize aria-label="empty textarea" placeholder="Empty" />
        {props.post.content} edit
    </Typography>
</CardContent>
</Card> */}


