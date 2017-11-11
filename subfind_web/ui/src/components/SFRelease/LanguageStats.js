import React from "react";

export default class LanguageStats extends React.Component {
  render() {
    let data = [];
    for (let lang of Object.keys(this.props.data)) {
      data.push({ lang: lang, size: this.props.data[lang].length });
    }

    return (
      <div className="">
        {data.map((item, k) => {
          return (
            <span style={{ paddingRight: "5px" }} key={k}>
              <strong>{item.lang}</strong>: {item.size} /
            </span>
          );
        })}
      </div>
    );
  }
}
