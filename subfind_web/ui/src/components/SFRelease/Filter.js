import React from "react";
import update from "react-addons-update";
import * as tb from "tb-react";
import { Switch } from "antd";
import { updateShowMissed, updateShowLang } from "../../actions";
import { connect } from "react-redux";

class SFReleaseFilter extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      languages: ["en", "vi"],
      filter: {
        empty: false,
        lang_en: false,
        lang_vi: false,
      },
    };
  }

  async toggleFilter(fieldName) {
    await this.setState(
      update(this.state, {
        filter: {
          [fieldName]: {
            $set: !this.state.filter[fieldName],
          },
        },
      })
    );

    if (this.props.onChange) {
      this.props.onChange(this.state.filter);
    }
  }

  render() {
    const {
      filter: { showMissed, onlyShowLang },
      setShowMissed,
      setShowLang,
    } = this.props;
    // console.log(onlyShowLang);
    return (
      <div>
        <div className="row">
          <div className="col-md-6 col-xs-8">
            Only show missed subtitle release
          </div>
          <div className="col-md-6 col-xs-4">
            <Switch defaultChecked={showMissed} onChange={setShowMissed} />
          </div>
        </div>
        {this.state.languages.map((lang, k) => {
          return (
            <div className="row" key={k}>
              <div className="col-md-6 col-xs-8">
                Only show missed lang {lang}
              </div>
              <div className="col-md-6 col-xs-4">
                <Switch
                  defaultChecked={onlyShowLang.indexOf(lang) >= 0}
                  onChange={() => setShowLang(lang)}
                />
              </div>
            </div>
          );
        })}
      </div>
    );
  }
}

const mapStateToProps = state => {
  return {
    filter: state.filter,
  };
};

const mapDispatchToProps = (dispatch: Function) => {
  return {
    setShowMissed: value => dispatch(updateShowMissed(value)),
    setShowLang: lang => dispatch(updateShowLang(lang)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(SFReleaseFilter);
