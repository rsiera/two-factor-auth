// @flow
import * as actionTypes from '../actions/actionTypes';

type DataReducerState = {
  data: {},
};

const initialState = {
  data: {},
};


const dataReducer = (state: DataReducerState = initialState, action: Object): DataReducerState => {
  switch(action.type) {
    case actionTypes.FETCH_PRIVATE_DATA_SUCCESS:
      state = {
        ...state,
        data: action.payload.data,
      };
      break;
    default:
      break;
  }
  return state;
};

export default dataReducer;
