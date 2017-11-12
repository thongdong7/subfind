import React from "react";
import { connect } from "react-redux";
import { Row, Col, Switch, Card } from "antd";
import { updateShowMissed, updateShowLang } from "../../actions";

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
      {
        filter: {
          ...this.state.filter,
          [fieldName]: !this.state.filter[fieldName],
        },
      }
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
      <Card>
        <Row>
          <Col span={12}>Only show missed subtitle release</Col>
          <Col span={12}>
            <Switch defaultChecked={showMissed} onChange={setShowMissed} />
          </Col>
        </Row>

        {this.state.languages.map((lang, k) => {
          return (
            <Row key={k}>
              <Col span={12}>
                Only show missed lang {lang}
              </Col>
              <Col span={12}>
                <Switch
                  defaultChecked={onlyShowLang.indexOf(lang) >= 0}
                  onChange={() => setShowLang(lang)}
                />
              </Col>
            </Row>
          );
        })}
      </Card>
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
