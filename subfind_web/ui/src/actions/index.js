export const SET_SHOW_MISSED = "SET_SHOW_MISSED";
export const SET_SHOW_LANG = "SET_SHOW_LANG";
export const UPDATE_RELEASES = "UPDATE_RELEASES";
export const RELEASE_LOADING = "RELEASE_LOADING";

export function loadReleases() {
  return async dispatch => {
    console.log("load releases");
    dispatch({
      type: RELEASE_LOADING,
    });

    const res = await fetch(`/api/Release/list`);
    const data = await res.json();
    // console.log("a", data);

    dispatch(updateReleases(data));
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
