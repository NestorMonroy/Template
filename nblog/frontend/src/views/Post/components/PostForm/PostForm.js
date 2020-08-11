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

    const fileInputRef = useRef(null);

    const handleChange = (event) => {
        event.persist();
        setValue(event.target.value);
    };


  const handleAttach = () => {
    fileInputRef.current.click();
  };


    return (
        <Card
            className={classes.root}
            // className={clsx(classes.root, className)}
        >
            <CardContent className={classes.content}>
                <Paper
                    className={classes.paper}
                    elevation={1}
                >
                    <Input
                        className={classes.input}
                        disableUnderline
                        onChange={handleChange}
                        placeholder={`What's on your mind, Nestor`}
                    />
                </Paper>
                <Tooltip title="Send">
                    <IconButton color={value.length > 0 ? 'primary' : 'default'}>
                        <SendIcon />
                    </IconButton>
                </Tooltip>
                <Divider className={classes.divider} />
                <Tooltip title="Attach image">
                    <IconButton
                        edge="end"
                        onClick={handleAttach}
                    >
                        <AddPhotoIcon />
                    </IconButton>
                </Tooltip>
                <Tooltip title="Attach file">
                    <IconButton
                        edge="end"
                        onClick={handleAttach}
                    >
                        <AttachFileIcon />
                    </IconButton>
                </Tooltip>
                <input
                    className={classes.fileInput}
                    ref={fileInputRef}
                    type="file"
                />
            </CardContent>
        </Card>
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


