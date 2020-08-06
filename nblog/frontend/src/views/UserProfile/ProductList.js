// import React, {useEffect, useState} from "react";
// import {productService} from "../../services/productService";
// import ProductCard from "./ProductCard";
// import Grid from "@material-ui/core/Grid";

// function ProductList() {
//   const [products, setProducts] = useState([]);

//   useEffect(() => {
//     productService
//       .findAll()
//       .then(products => setProducts(products))
//   },[]);

// return (
//     <Grid
//       container
//       spacing={3}
//     >
//       {products.map(p => (
//         <Grid
//           item
//           key={p.id}
//           lg={4}
//           lx={4}
//           md={6}
//           xs={12}
//         >
//           <ProductCard product={p}/>
//         </Grid>
//       ))}
//     </Grid>
// )
// }

// export default ProductList;
