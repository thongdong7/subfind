import { SET_SHOW_MISSED, SET_SHOW_LANG } from "../actions";
const initState = {
  showMissed: false,
  onlyShowLang: [],
};

export default function reducer(state = initState, action) {
  switch (action.type) {
    case SET_SHOW_MISSED:
      return {
        ...state,
        showMissed: action.payload,
      };
    case SET_SHOW_LANG:
      const { lang } = action;
      let { onlyShowLang } = state;
      if (onlyShowLang.indexOf(lang) < 0) {
        onlyShowLang = [...onlyShowLang, lang];
      } else {
        onlyShowLang = onlyShowLang.filter(l => l !== lang);
      }

      return {
        ...state,
        onlyShowLang,
      };
    default:
      return state;
  }
}
