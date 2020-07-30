import {Dialog} from "@material-ui/core";
import PropTypes from "prop-types";
import React, {useEffect, useState} from "react";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContent from "@material-ui/core/DialogContent";
import TextField from "@material-ui/core/TextField";
import DialogActions from "@material-ui/core/DialogActions";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import makeStyles from "@material-ui/core/styles/makeStyles";
import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import {categoryService} from "../../services/categoryService";
import {subCategoryService} from "../../services/subCategoryService";
import {useForm} from "react-hook-form";
import FormHelperText from "@material-ui/core/FormHelperText";
import {productService} from "../../services/productService";

const useStyles = makeStyles(theme => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
  input: {
    display: 'none',
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
}));

function AddProductDialog({open, onClose}) {
  const classes = useStyles();
  const [categories, setCategories] = useState([]);
  const [subCategories, setSubCategories] = useState([]);

  const {register, setValue, handleSubmit, errors} = useForm();

  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedSubCategory, setSelectedSubCategory] = useState('');

  useEffect(() => {
    register({name: "category"}, {required: "Category is required"});
    register({name: "subCategory"}, {required: "SubCategory is required"});
  }, [register]);

  useEffect(() => {
    categoryService
      .findAll()
      .then(categories => setCategories(categories))
  }, []);

  const handleCategoryChange = (e) => {
    const value = e.target.value;
    setSelectedCategory(value);
    setValue("category", value);

    if (!value) {
      setSubCategories([]);
    }

    subCategoryService
      .findAllByCategory(value)
      .then(subCategories => setSubCategories(subCategories))
  };

  const handleSubCategoryChange = (e) => {
    const value = e.target.value;
    setSelectedSubCategory(value);
    setValue("subCategory", value);
  };


  const handleSave = (data) => {
    const {name, price, description, subCategory} = data;
    productService.saveProduct(name, price, description, subCategory);
    onClose();
  };

  return (
    <Dialog open={open} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Add a product</DialogTitle>
      <DialogContent>

        <Grid container spacing={2}>
          <Grid item md={6}>
            <TextField
              autoFocus
              margin="dense"
              name="name"
              label="Name"
              type="text"
              error={Boolean(errors.name)}
              helperText={errors.name ? errors.name.message : null}
              inputRef={register({
                required: "Name is required"
              })}
            />
          </Grid>
          <Grid item md={6}>
            <TextField
              autoFocus
              margin="dense"
              name="price"
              label="Price"
              type="number"
              error={Boolean(errors.price)}
              helperText={errors.price ? errors.price.message : null}
              inputRef={register({
                required: "Price is required"
              })}
            />
          </Grid>
          <Grid item md={6}>
            <TextField
              autoFocus
              margin="dense"
              name="description"
              label="Description"
              type="text area"
              error={Boolean(errors.description)}
              helperText={errors.description ? errors.description.message : null}
              inputRef={register({
                required: "Description is required"
              })}
            />
          </Grid>
          <Grid item md={6}>
            <FormControl className={classes.formControl} error={Boolean(errors.category)}>
              <InputLabel id="category">Category</InputLabel>
              <Select
                name="category"
                value={selectedCategory}
                onChange={handleCategoryChange}
              >
                <MenuItem value=""/>
                {categories.map(c =>
                  <MenuItem key={c.id} value={c.id}>{c.name}</MenuItem>
                )}
              </Select>
              {errors.category && <FormHelperText error>{errors.category.message}</FormHelperText>}
            </FormControl>
          </Grid>
          <Grid item md={6}>
            <FormControl className={classes.formControl} error={Boolean(errors.subCategory)}>
              <InputLabel id="subCategory">SubCategory</InputLabel>
              <Select
                name="subCategory"
                value={selectedSubCategory}
                onChange={handleSubCategoryChange}
              >
                <MenuItem value=""/>
                {subCategories.map(s =>
                  <MenuItem key={s.id} value={s.id}>{s.name}</MenuItem>
                )}
              </Select>
              {errors.subCategory && <FormHelperText error>{errors.subCategory.message}</FormHelperText>}
            </FormControl>
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button color="primary" onClick={onClose}>
          Cancel
        </Button>
        <Button color="primary" onClick={handleSubmit(handleSave)}>
          Save
        </Button>
      </DialogActions>
    </Dialog>
  )
}

AddProductDialog.propTypes = {
  open: PropTypes.bool,
  onClose: PropTypes.func,
  onSave: PropTypes.func,
};

export default AddProductDialog;
