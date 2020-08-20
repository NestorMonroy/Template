import React, {useState} from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/styles';
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

import Markdown from 'src/components/Markdown';

import StarRateIcon from '@material-ui/icons/StarRate';

const useStyles = makeStyles(() => ({
  root: {}
}));

const Content = props => {
  const {  className, ...rest } = props;
  const classes = useStyles();

  const [ highlighted, setHighlihted] = useState(-1);

  //let pos = props.posts;

  const highlightRate = high => evt => {
    setHighlihted(high)
  }
  
  return (
    <Card

    >
      <CardContent>
      
      </CardContent>
      <Container maxWidth="md" component="main">
          {/* <Grid container spacing={2} alignItems="flex-end">
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
                      return <IconButton key={i} className={highlighted > i - 1 ? classes.rateButton1 : classes.rateButton}
                        onMouseEnter={highlightRate(i)}
                        onMouseLeave={highlightRate(-1)}
                        onClick={(i)}
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
                    {/* </ul>
                  </CardContent>
                  <CardActions>
                    <Button fullWidth color="primary">

                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ) : null}
          </Grid> */}
        </Container>
    </Card>
  );
};

Content.propTypes = {
  //content: PropTypes.string.isRequired,
  className: PropTypes.string
};

export default Content;
