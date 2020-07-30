import makeStyles from "@material-ui/core/styles/makeStyles";
import TreeView from "@material-ui/lab/TreeView";
import React, {useEffect, useState} from "react";
import TreeItem from "@material-ui/lab/TreeItem";
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import {categoryService} from "../../services/categoryService";
import {subCategoryService} from "../../services/subCategoryService";
import PropTypes from "prop-types";

const useStyles = makeStyles({
  root: {
    height: 240,
    flexGrow: 1,
    maxWidth: 400,
  },
});

function CategoryTree({onCategoryClick, onSubCategoryClick}) {
  const classes = useStyles();
  const [categories, setCategories] = useState([]);
  const [subCategories, setSubCategories] = useState([]);

  useEffect(() => {
      categoryService
        .findAll()
        .then(categories => setCategories(categories));

      subCategoryService
        .findAll()
        .then(subCategories => setSubCategories(subCategories));
    }
    , []);

  return (

    <TreeView
      className={classes.root}
      defaultCollapseIcon={<ExpandMoreIcon/>}
      defaultExpandIcon={<ChevronRightIcon/>}
    >
      {categories.map(c =>
        <TreeItem key={`cat_${c.id}`} nodeId={`cat_${c.id}`} label={c.name}
                  onClick={() => onCategoryClick(c.id)}>
          {subCategories.filter(s => s.category.id === c.id).map(s =>
            <TreeItem key={`subcat_${s.id}`} nodeId={`subcat_${s.id}`} label={s.name}
                      onClick={() => onSubCategoryClick(s.id)}/>
          )}
        </TreeItem>
      )}
    </TreeView>
  );
}

CategoryTree.propTypes = {
  onCategoryClick: PropTypes.func,
  onSubCategoryClick: PropTypes.func,
};

export default CategoryTree;
