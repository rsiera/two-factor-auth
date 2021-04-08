// @flow
import * as actionTypes from './actionTypes';

const loginUserSuccess = (data: Object) => {
    localStorage.setItem('token', data.token);
    return {
        type: actionTypes.LOGIN_USER_SUCCESS,
        payload: {
            data,
        },
    };
}

const logout = () => {
    localStorage.removeItem('token');
    return {
        type: actionTypes.LOGOUT_USER,
    };
}
export {
  loginUserSuccess,
  logout
};
