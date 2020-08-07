import React, {useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import StarRateIcon from '@material-ui/icons/StarRate';
// import StarOutlineIcon from '@material-ui/icons/StarOutline';

import {
    Container,
    Paper,
    Typography,
    Grid,
    IconButton,
    Divider,
    Card,
    CardActions,
    CardContent,
    CardHeader,
    Button

} from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
    root: {},
    content: {
        display: 'flex',
        alignItems: 'center'
    },
    cardHeader: {
        backgroundColor:
            theme.palette.type === 'light' ? theme.palette.grey[200] : theme.palette.grey[700],
    },
    cardPricing: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'baseline',
        marginBottom: theme.spacing(2),
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
        lineHeight: '5px'
    },
    starButton: {
        // display: 'none',
        // color: 'orange',
        marginLeft: theme.spacing(1)
    },
    starButton2: {
        // display: 'none',
        color: 'orange',
        marginLeft: theme.spacing(1)
    },
    rateButton:{
        // size='2rem',
        marginLeft: theme.spacing(1)
    },
    rateButton1: {
        // display: 'none',
        color: 'red',
        marginLeft: theme.spacing(1)
    },
    divider: {
        margin: theme.spacing(2, 0),
    },
}));


function PostDetails(props) {
    const { className, } = props;
    const classes = useStyles();

    const [ highlighted, setHighlihted] = useState(-1);

    const pos = props.post;

    const highlightRate = high => evt => {
        setHighlihted(high)
    }

    const rateClicked = rate => evt => {
        fetch(`http://127.0.0.1:8000/api/post/posts/${pos.id}/rate_post/`, {
            method: 'POST',
            headers: {
                  'Content-Type': 'application/json',
                  'Authorization': 'Token 6165f2762ac4358af1bdfceab20bb75b15d976d6'
            },
            body: JSON.stringify( {stars: rate +1} )
          })
          .then(resp => resp.json())
          .then( resp => console.log(resp))
          .catch(error => console.log(error))

    }


    return (
        <Container maxWidth="md" component="main">
            <Grid container spacing={2} alignItems="flex-end">
                {pos ? (
                    <Grid item xs={12}>
                        <Card>
                            <CardHeader
                                title={pos.content}
                                titleTypographyProps={{ align: 'center' }}
                                subheaderTypographyProps={{ align: 'center' }}
                                className={classes.cardHeader}
                            />
                            <CardContent>
                                <div className={classes.cardPricing}>
                                    <Typography>
                                        <IconButton className={pos.avg_rating > 0 ? classes.starButton2 : classes.starButton}>
                                            <StarRateIcon />
                                        </IconButton>
                                        <IconButton className={pos.avg_rating > 1 ? classes.starButton2 : classes.starButton}>
                                            <StarRateIcon />
                                        </IconButton>
                                        <IconButton className={pos.avg_rating > 2 ? classes.starButton2 : classes.starButton}>
                                            <StarRateIcon />
                                        </IconButton>
                                        <IconButton className={pos.avg_rating > 3 ? classes.starButton2 : classes.starButton}>
                                            <StarRateIcon />
                                        </IconButton>
                                        <IconButton className={pos.avg_rating > 4 ? classes.starButton2 : classes.starButton}>
                                            <StarRateIcon />
                                        </IconButton>
                                    </Typography>

                                    <Typography component="h2" variant="h3" color="textPrimary">
                                        ({pos.no_of_ratings})
                                    </Typography>
                                </div>
                                <Divider className={classes.divider} />

                                <Typography component="h2" variant="subtitle1" align="center">
                                    Rate it
                                </Typography>
                                {[...Array(5)].map((e, i) => {
                                    return <IconButton  key={i} className={highlighted > i -1 ? classes.rateButton1 : classes.rateButton}
                                            onMouseEnter={highlightRate(i)}
                                            onMouseLeave={highlightRate(-1)}
                                            onClick={rateClicked(i)}
                                            >
                                                <StarRateIcon />
                                            </IconButton>
                                })}
                                <ul>


                                    {/* {tier.description.map((line) => (
                                        <Typography component="li" variant="subtitle1" align="center" key={line}>
                                            {line}
                                        </Typography>
                                    ))} */}
                                </ul>
                            </CardContent>
                            <CardActions>
                                <Button fullWidth color="primary">

                                </Button>
                            </CardActions>
                        </Card>
                    </Grid>
                ) : null}
            </Grid>
        </Container>
    )
}
export default PostDetails;