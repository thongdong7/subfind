import { combineReducers } from "redux";

import filter from "./filter";
import releases from "./releases";

export default combineReducers({
  filter,
  releases,
});
