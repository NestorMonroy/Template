import React, {Fragment, useEffect, useState} from "react";
import Grid from "@material-ui/core/Grid";
import ProductDisplay from "./ProductDisplay";
import PropTypes from "prop-types";
import CategoryTree from "./CategoryTree";
import {productService} from "../../services/productService";
import {Typography} from "@material-ui/core";

function ProductGrid({products}) {
  return (
    <Fragment>
      <Grid container>
        {products.map(p =>
          <Grid key={p.id} item md={6}>
            <ProductDisplay product={p}/>
          </Grid>)}
      </Grid>
    </Fragment>
  )
}

export default ProductGrid;
