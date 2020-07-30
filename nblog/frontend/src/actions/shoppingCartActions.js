export const SHOPPING_CART_ADD_PRODUCT = "SHOPPING_CART_ADD_PRODUCT";

export const shoppingCartActions = {
  addProduct,
}

function addProduct(product) {
  return dispatch => dispatch({
      type: SHOPPING_CART_ADD_PRODUCT,
      product
    })
}
