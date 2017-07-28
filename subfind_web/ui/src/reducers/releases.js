import { UPDATE_RELEASES, RELEASE_LOADING } from "../actions";

const initState = {
  items: [],
  loading: false,
};

export default function reducer(state = initState, action) {
  switch (action.type) {
    case UPDATE_RELEASES:
      return {
        items: action.releases,
        loading: false,
      };
    case RELEASE_LOADING:
      return {
        ...state,
        loading: true,
      };
    default:
      return state;
  }
}
