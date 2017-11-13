import { Button, Col, Form, Input, Row, Switch as UISwitch } from "antd";
import React, { Component } from "react";
import { connect } from "react-redux";
import compose from "recompose/compose";
import RPCButton from "../RPCButton";
import MovieFolder from "./MovieFolder";
const FormItem = Form.Item;

let mb = 1024 * 1024;

const FormRow = ({ children }) => {
  return (
    <div className="row">
      <div className="col-sm-3">{children[0]}</div>
      <div className="col-sm-9">{children[1]}</div>
    </div>
  );
};

const builtinProviders = [
  { name: "opensubtitles", displayName: "Opensubtitles" },
  { name: "subscene", displayName: "Subscene" },
];

const configActions = {};
const formItemLayout = {
  labelCol: {
    xs: { span: 24 },
    sm: { span: 6 },
  },
  wrapperCol: {
    xs: { span: 24 },
    sm: { span: 14 },
  },
};
const tailFormItemLayout = {
  wrapperCol: {
    xs: {
      span: 24,
      offset: 0,
    },
    sm: {
      span: 14,
      offset: 6,
    },
  },
};

class SFConfigIndex extends Component {
  render() {
    const {
      config: { src: folders, lang: languages, providers, force, remove },
    } = this.props;
    const { getFieldDecorator } = this.props.form;

    // console.log('config', this.props.config);
    const config = this.props.config;

    return (
      <div className="box box-solid">
        <div className="box-header with-border">
          <h3 className="box-title">
            <Button>Back</Button>
          </h3>
        </div>
        <div className="box-body">
          <div style={{ margin: 10 }}>
            <Row>
              <Col span={12}>
                <strong>Movie Folders</strong>
              </Col>
              <Col span={12}>
                {folders.map((folder, k) => {
                  return (
                    <MovieFolder src={folder} key={k}>
                      <RPCButton
                        name="Remove"
                        icon="delete"
                        hideName
                        type="danger"
                        action={[
                          configActions.updateListField,
                          "src",
                          folder,
                          false,
                        ]}
                      />
                    </MovieFolder>
                  );
                })}
                <Input
                  actionFunc={value => [
                    configActions.updateListField,
                    "src",
                    value,
                    true,
                  ]}
                />
              </Col>
            </Row>
            <Row>
              <Col span={12}>
                <strong>Languages</strong>
              </Col>
              <Col span={12}>
                {languages.map((lang, k) => {
                  return (
                    <MovieFolder src={lang} key={k}>
                      <RPCButton
                        name="Remove"
                        icon="delete"
                        hideName
                        type="danger"
                        action={[
                          configActions.updateListField,
                          "lang",
                          lang,
                          false,
                        ]}
                      />
                    </MovieFolder>
                  );
                })}

                <Input
                  actionFunc={value => [
                    configActions.updateListField,
                    "lang",
                    value,
                    true,
                  ]}
                />
              </Col>
            </Row>
            <Row>
              <Col span={12}>
                <strong>Providers</strong>
              </Col>
              <Col span={12}>
                {builtinProviders.map(
                  ({ name: providerName, displayName }, k) => {
                    let checked = providers.indexOf(providerName) >= 0;
                    return (
                      <div key={k}>
                        <div className="col-sm-3">{displayName}</div>
                        <div className="col-sm-9">
                          <UISwitch
                            checked={checked}
                            action={[
                              configActions.updateListField,
                              "providers",
                              providerName,
                            ]}
                          />
                        </div>
                      </div>
                    );
                  }
                )}
              </Col>
            </Row>
            <Row>
              <Col span={12}>
                <strong>Force download subtitle</strong>
              </Col>
              <Col span={12}>
                <UISwitch
                  checked={force}
                  action={[configActions.updateField, "force"]}
                />
              </Col>
            </Row>
            <Row>
              <Col span={12}>
                <strong>Remove old subtitles if not found new subtitle</strong>
              </Col>
              <Col span={12}>
                <UISwitch
                  checked={remove}
                  action={[configActions.updateField, "remove"]}
                />
              </Col>
            </Row>
            <Row>
              <Col span={12}>
                <strong>Min movie size (MB)</strong>
                <div>(to ignore sample videos)</div>
              </Col>
              <Col span={12}>
                <Input
                  value={config["min-movie-size"] / mb}
                  actionFunc={value => [
                    configActions.updateField,
                    "min-movie-size",
                    Number(value) * mb,
                  ]}
                />
              </Col>
            </Row>
            <Row>
              <Col span={12}>
                <strong>Number subtitles</strong>
              </Col>
              <Col span={12}>
                <Input
                  value={config["max-sub"]}
                  action={[configActions.updateField, "max-sub"]}
                />
              </Col>
            </Row>
          </div>
        </div>
      </div>
    );
  }
}

// SFConfigIndex.contextTypes = {
//     router: React.PropTypes.object
// }

// export default tb.connect2({
//   start: dispatch => {
//     dispatch(configActions.load);
//   },
//   props: ({ config }, ownProps, dispatch) => ({
//     config,
//   }),
// })(SFConfigIndex);

const mapStateToProps = state => {
  return {
    config: {
      src: ["/data"],
      lang: ["vi", "en"],
      providers: ["opensubtitles", "subscene"],
    },
  };
};

const enhance = compose(Form.create(), connect(mapStateToProps));

export default enhance(SFConfigIndex);
