import React, { useState, useRef, useEffect } from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/styles';
import {
  Button,
  Grid,
  Menu,
  MenuItem,
  ListItemText,
  Typography
} from '@material-ui/core';
import { ToggleButtonGroup, ToggleButton } from '@material-ui/lab';
import ViewModuleIcon from '@material-ui/icons/ViewModule';
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';

import axios from 'src/utils/axios';
import Paginate from 'src/components/Paginate';
import ProjectCard from 'src/components/ProjectCard';

const useStyles = makeStyles(theme => ({
  root: {},
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    flexWrap: 'wrap',
    marginBottom: theme.spacing(2)
  },
  title: {
    position: 'relative',
    '&:after': {
      position: 'absolute',
      bottom: -8,
      left: 0,
      content: '" "',
      height: 3,
      width: 48,
      backgroundColor: theme.palette.primary.main
    }
  },
  actions: {
    display: 'flex',
    alignItems: 'center'
  },
  sortButton: {
    textTransform: 'none',
    letterSpacing: 0,
    marginRight: theme.spacing(2)
  },
  paginate: {
    marginTop: theme.spacing(3),
    display: 'flex',
    justifyContent: 'center'
  }
}));

const Projects = props => {
  const { className, ...rest } = props;

  const classes = useStyles();
  const sortRef = useRef(null);
  const [openSort, setOpenSort] = useState(false);
  const [selectedSort, setSelectedSort] = useState('Most popular');
  const [mode, setMode] = useState('grid');
  const [projects, setProjects] = useState([]);

  // useEffect(() => {
  //   fetch("http://127.0.0.1:8000/api/post/posts/", {
  //     method: 'GET',
  //     headers: {
  //       'Content-Type': 'application/json',
  //       'Authorization': 'Token 6165f2762ac4358af1bdfceab20bb75b15d976d6'
  //     }
  //   })
  //     .then(resp => resp.json())
  //     .then(resp => setProjects(resp))
  //     .catch(error => console.log(error))


  // }, [])

  // const apiPost = axios.create({
  //   baseURL: `http://127.0.0.1:8000/api/post/posts/`
  // })

  useEffect(() => {

    axios.get('api/post/posts/')
      .then(response => {
        setProjects(response.data);
        console.log(response)
      })
      .catch(error => console.log(error))

    // const fetchProjects = () => {
    //   axios.get('http://127.0.0.1:8000/api/post/posts/').then(response => {
    //       setProjects(response.data.projects);
    //   });
    // };

    // fetchProjects();

    // return () => {
    //   console.log('return algo 2')
    // };
  }, []);


  const handleSortOpen = () => {
    setOpenSort(true);
  };

  const handleSortClose = () => {
    setOpenSort(false);
  };

  const handleSortSelect = value => {
    setSelectedSort(value);
    setOpenSort(false);
  };

  const handleModeChange = (event, value) => {
    setMode(value);
  };

  return (
    <div
      {...rest}
      className={clsx(classes.root, className)}
    >
      <div className={classes.header}>
        <Typography
          className={classes.title}
          variant="h5"
        >
          Showing projects
        </Typography>
        <div className={classes.actions}>
          <Button
            className={classes.sortButton}
            onClick={handleSortOpen}
            ref={sortRef}
          >
            {selectedSort}
            <ArrowDropDownIcon />
          </Button>
          <ToggleButtonGroup
            exclusive
            onChange={handleModeChange}
            size="small"
            value={mode}
          >
            <ToggleButton value="grid">
              <ViewModuleIcon />
            </ToggleButton>
          </ToggleButtonGroup>
        </div>
      </div>
      <Grid
        container
        spacing={3}
      >
        {projects.map(project => (
          <Grid
            item
            key={project.id}
            md={mode === 'grid' ? 4 : 12}
            sm={mode === 'grid' ? 6 : 12}
            xs={12}
          >
           <ProjectCard project={project} />
          </Grid>
        ))}
      </Grid>
      <div className={classes.paginate}>
        <Paginate pageCount={3} />
      </div>
      <Menu
        anchorEl={sortRef.current}
        className={classes.menu}
        onClose={handleSortClose}
        open={openSort}
      >
        {['Most recent', 'Popular', 'Price high', 'Price low', 'On sale'].map(
          option => (
            <MenuItem
              className={classes.menuItem}
              key={option}
              onClick={() => handleSortSelect(option)}
            >
              <ListItemText primary={option} />
            </MenuItem>
          )
        )}
      </Menu>
    </div>
  );
};

Projects.propTypes = {
  className: PropTypes.string
};

export default Projects;
