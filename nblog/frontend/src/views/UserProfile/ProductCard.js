// import React, { useState } from 'react';
// import { Link as RouterLink } from 'react-router-dom';
// import PropTypes from 'prop-types';
// import clsx from 'clsx';
// import { makeStyles } from '@material-ui/styles';
// import {
//   Avatar,
//   Button,
//   Card,
//   CardContent,
//   CardHeader,
//   Divider,
//   Grid,
//   IconButton,
//   Link,
//   Tooltip,
//   Typography,
//   colors
// } from '@material-ui/core';
// import AddShoppingCartIcon from '@material-ui/icons/AddShoppingCart';
// import ButtonBase from "@material-ui/core/ButtonBase";
// import {useDispatch} from "react-redux";
// import {shoppingCartActions} from "../../actions";

// const useStyles = makeStyles((theme) => ({
//   root: {},
//   header: {
//     paddingBottom: 0
//   },
//   content: {
//     padding: 0,
//     '&:last-child': {
//       paddingBottom: 0
//     }
//   },
//   description: {
//     padding: theme.spacing(2, 3, 1, 3)
//   },
//   cartButton: {
//     marginLeft: theme.spacing(1)
//   },
//   details: {
//     padding: theme.spacing(2, 3)
//   },
//   image: {
//     width: 250,
//     height: 250,
//   },
//   img: {
//     margin: 'centered',
//     display: 'block',
//     maxWidth: '100%',
//     maxHeight: '100%',
//   },
// }));

// function ProductCard({ product, className, ...rest }) {
//   const classes = useStyles();

//   const dispatch = useDispatch();

//   const handleAddToCart = () => {
//     dispatch(shoppingCartActions.addProduct(product))
//   };

//   return (
//     <Card>
//       <CardHeader
//         title={(
//           <Link
//             color="textPrimary"
//             component={RouterLink}
//             to="/profile"
//             variant="h5"
//           >
//             {product.name}
//           </Link>
//         )}
//       />
//       <CardContent className={classes.content}>
//         <ButtonBase className={classes.image}>
//           <img className={classes.img} alt="complex" src={product.image} />
//         </ButtonBase>
//         <Divider />
//         <div className={classes.details}>
//           <Grid
//             alignItems="center"
//             container
//             justify="space-between"
//             spacing={3}
//           >
//             <Grid item>
//               <Typography variant="h5">
//                 ${product.price}
//               </Typography>
//             </Grid>
//             <Grid item>
//               <Typography variant="h5">{product.subCategory.category.name}</Typography>
//               <Typography variant="body2">Category</Typography>
//             </Grid>
//             <Grid item>
//               <Typography variant="h5">{product.subCategory.name}</Typography>
//               <Typography variant="body2">SubCategory</Typography>
//             </Grid>
//             <Grid item>
//               <Tooltip title="Add to Cart">
//                 <IconButton
//                   className={classes.cartButton}
//                   size="small"
//                 >
//                   <AddShoppingCartIcon onClick={(product) => handleAddToCart(product)}/>
//                 </IconButton>
//               </Tooltip>
//             </Grid>
//           </Grid>
//         </div>
//       </CardContent>
//     </Card>
//   );
// }

// ProductCard.propTypes = {
//   className: PropTypes.string,
//   product: PropTypes.object.isRequired
// };

// export default ProductCard;
