import { Alert, Button, Col, Form, Input, Row, Switch as UISwitch } from "antd";
import React, { Component } from "react";
import { connect } from "react-redux";
import compose from "recompose/compose";
import { loadConfig, updateConfigListField } from "../../actions";
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

class InlineInput extends Component {
  render() {
    return (
      <Input {...this.props} onPressEnter={e => console.log(e.target.value)} />
    );
  }
}

class SFConfigIndex extends Component {
  componentDidMount() {
    this.props.loadConfig();
  }

  render() {
    const {
      config: { src: folders, lang: languages, providers, force, remove },
      updateListField,
      errorMessage,
    } = this.props;

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
            {errorMessage && <Alert type="error" message={errorMessage} />}
            <Row>
              <Col span={12}>
                <strong>Movie Folders</strong>
              </Col>
              <Col span={12}>
                {folders.map((folder, k) => {
                  return (
                    <MovieFolder src={folder} key={k}>
                      <Button
                        name="Remove"
                        icon="delete"
                        hideName
                        type="danger"
                        onClick={() =>
                          updateListField({
                            field: "src",
                            value: folder,
                            action: "remove",
                          })}
                      >
                        Remove
                      </Button>
                    </MovieFolder>
                  );
                })}
                <Input
                  onPressEnter={e =>
                    updateListField({
                      field: "src",
                      value: e.target.value,
                      action: "add",
                    })}
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
                      <Button
                        name="Remove"
                        icon="delete"
                        hideName
                        type="danger"
                        onClick={() =>
                          updateListField({
                            field: "lang",
                            value: lang,
                            action: "remove",
                          })}
                      >
                        Remove
                      </Button>
                    </MovieFolder>
                  );
                })}

                <Input
                  onPressEnter={e =>
                    updateListField({
                      field: "lang",
                      value: e.target.value,
                      action: "add",
                    })}
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
                    const checked = providers.indexOf(providerName) >= 0;

                    return (
                      <div key={k}>
                        <div className="col-sm-3">{displayName}</div>
                        <div className="col-sm-9">
                          <UISwitch
                            checked={checked}
                            onChange={isChecked => {
                              updateListField({
                                field: "providers",
                                value: providerName,
                                action: isChecked ? "add" : "remove",
                              });
                            }}
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
      ...state.config.config,
    },
    ...state.config,
  };
};

const mapDispatchToProps = (dispatch: Function) => {
  return {
    loadConfig: () => {
      dispatch(loadConfig());
    },
    updateListField: ({ field, value, action }) => {
      dispatch(updateConfigListField({ field, value, action }));
    },
  };
};

const enhance = compose(
  Form.create(),
  connect(mapStateToProps, mapDispatchToProps)
);

export default enhance(SFConfigIndex);
