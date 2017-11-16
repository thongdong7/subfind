import { uniq } from "lodash";
import { UPDATE_CONFIG, UPDATE_CONFIG_ERROR } from "../actions";

const initState = {
  loaded: false,
  errorMessage: null,
  config: {
    src: [],
    lang: [],
    providers: [],
  },
};

export default function reducer(state = initState, action) {
  switch (action.type) {
    case UPDATE_CONFIG:
      return {
        ...state,
        errorMessage: null,
        loaded: true,
        config: action.payload,
      };
    case UPDATE_CONFIG_ERROR:
      return {
        ...state,
        loaded: true,
        errorMessage: action.payload,
      };
    case "ADD_CONFIG_LIST_FIELD": {
      const { field, value } = action.payload;
      return {
        ...state,
        config: {
          ...state.config,
          [field]: uniq([...state.config[field], value]),
        },
      };
    }
    case "REMOVE_CONFIG_LIST_FIELD": {
      const { field, value } = action.payload;
      return {
        ...state,
        config: {
          ...state.config,
          [field]: state.config[field].filter(item => item !== value),
        },
      };
    }
    default:
      return state;
  }
}
