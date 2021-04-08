// @flow
import * as actionTypes from '../actions/actionTypes';
import jwtDecode from "jwt-decode";

type AuthReducerState = {
  isAuthenticated: boolean,
  token: null,
  userName: null
};

const initialState = {
  isAuthenticated: false,
  token: null,
  userName: null,
};


const authReducer = (state: AuthReducerState = initialState, action: Object): AuthReducerState => {
  switch(action.type) {
    case actionTypes.LOGIN_USER_SUCCESS:
      state = {
        ...state,
        isAuthenticated: true,
        token: action.payload.data.token,
        userName: jwtDecode(action.payload.data.token)
      };
      break;
    case actionTypes.LOGIN_USER_FAILURE:
      state = {
        ...state,
       isAuthenticated: false,
       token: null,
       userName: null,
      };
      break;
    case actionTypes.LOGOUT_USER:
      state = {
        ...state,
        isAuthenticated: false,
        token: null,
        userName: null,
      };
      break;
    default:
      break;
  }
  return state;
};

export default authReducer;
