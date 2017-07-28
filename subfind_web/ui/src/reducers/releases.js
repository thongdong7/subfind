import { UPDATE_RELEASES } from "../actions";

const initState = [];

export default function reducer(state = initState, action) {
  switch (action.type) {
    case UPDATE_RELEASES:
      return action.releases;
    default:
      return state;
  }
}
