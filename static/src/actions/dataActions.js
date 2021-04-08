// @flow
import * as actionTypes from './actionTypes';

const fetchProtectedDataSuccess = (data: Object) => {
    return {
        type: actionTypes.FETCH_PRIVATE_DATA_SUCCESS,
        payload: {
            data,
        },
    };
}

export {
  fetchProtectedDataSuccess,
};
