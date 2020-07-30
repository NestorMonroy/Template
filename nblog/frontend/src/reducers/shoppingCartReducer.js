import {SHOPPING_CART_ADD_PRODUCT} from "../actions";

const initialState = {
  products: []
};

export const shoppingCartReducer = (state = initialState, action) => {
  switch (action.type) {
    case SHOPPING_CART_ADD_PRODUCT:
      const {product} = action;
      const {products, ...others} = state;
      return {
        products: [product, ...products],
        ...others
      };
    default:
      return state;
  }
};
