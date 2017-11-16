export const SET_SHOW_MISSED = "SET_SHOW_MISSED";
export const SET_SHOW_LANG = "SET_SHOW_LANG";
export const UPDATE_RELEASES = "UPDATE_RELEASES";
export const RELEASE_LOADING = "RELEASE_LOADING";
export const UPDATE_CONFIG_ERROR = "UPDATE_CONFIG_ERROR";
export const UPDATE_CONFIG = "UPDATE_CONFIG";

export function loadReleases() {
  return async dispatch => {
    dispatch({
      type: RELEASE_LOADING,
    });

    const res = await fetch(`/api/Release/list`);
    const data = await res.json();
    // console.log("a", data);

    return dispatch(updateReleases(data));
  };
}

export function updateReleases(releases) {
  return { type: UPDATE_RELEASES, releases };
}
export function updateShowMissed(payload) {
  return {
    type: SET_SHOW_MISSED,
    payload,
  };
}

export function updateShowLang(lang) {
  return { type: SET_SHOW_LANG, lang };
}

export function updateConfigError(message: string) {
  return {
    type: UPDATE_CONFIG_ERROR,
    payload: message,
  };
}

export function updateConfig(config) {
  return {
    type: UPDATE_CONFIG,
    payload: config,
  };
}

export function loadConfig() {
  return async dispatch => {
    const res = await fetch("/api/Config/load");
    const config = await res.json();

    // console.log("c", config);

    dispatch(updateConfig(config));
  };
}

export function updateConfigListField({ field, value, action }) {
  return async dispatch => {
    // const params = {
    //   field: action === "add" ? `${field}-$push` : `${field}-$remove`,
    //   value,
    // };

    dispatch({
      type:
        action === "add" ? "ADD_CONFIG_LIST_FIELD" : "REMOVE_CONFIG_LIST_FIELD",
      payload: {
        field,
        value,
      },
    });

    const field_ = action === "add" ? `${field}-$push` : `${field}-$remove`;

    // console.log("p", params);
    const res = await fetch(`/api/Config/update?${field_}=${value}`, {});
    const config = await res.json();
    // console.log("config", config);

    if (config.ok === false) {
      dispatch(updateConfigError(config.message));

      // revert if action is add
      if (action === "add") {
        dispatch({
          type: "REMOVE_CONFIG_LIST_FIELD",
          payload: {
            field,
            value,
          },
        });
      }
    } else {
      dispatch(updateConfig(config));
    }
  };
}

export function updateConfigField({ field, value }) {
  return async dispatch => {
    dispatch({
      type: "UPDATE_CONFIG_FIELD",
      payload: {
        field,
        value,
      },
    });

    // console.log("p", params);
    const res = await fetch(`/api/Config/update?${field}=${value}`, {});
    const config = await res.json();
    // console.log("config", config);

    if (config.ok === false) {
      dispatch(updateConfigError(config.message));
    } else {
      dispatch(updateConfig(config));
    }
  };
}
