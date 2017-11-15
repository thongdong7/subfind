import { combineReducers } from "redux";
import config from "./config";
import filter from "./filter";
import releases from "./releases";

export default combineReducers({
  filter,
  releases,
  config,
});
