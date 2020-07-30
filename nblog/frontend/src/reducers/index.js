import {combineReducers} from 'redux';
import {userReducer} from "./userReducer";
import {shoppingCartReducer} from "./shoppingCartReducer";

const rootReducer = combineReducers({
  userReducer,
  shoppingCartReducer
});

export default rootReducer;
