// @flow
import {
  Alert,
  Button,
  Col,
  Form,
  Input,
  message,
  Row,
  Switch as UISwitch,
} from "antd";
import React, { Component } from "react";
import { connect } from "react-redux";
import compose from "recompose/compose";
import {
  loadConfig,
  updateConfigField,
  updateConfigListField,
} from "../../actions";
import MovieFolder from "./MovieFolder";

const mb = 1024 * 1024;

const builtinProviders = [
  { name: "opensubtitles", displayName: "Opensubtitles" },
  { name: "subscene", displayName: "Subscene" },
];

const configActions = {};

class SFConfigIndex extends Component {
  componentDidMount() {
    this.props.loadConfig();
  }

  render() {
    const {
      config: { src: folders, lang: languages, providers, force, remove },
      updateListField,
      updateField,
      errorMessage,
      loaded,
    } = this.props;

    if (!loaded) {
      return <div>loading...M</div>;
    }

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
                  onChange={isChecked => {
                    updateField({
                      field: "force",
                      value: isChecked,
                    });
                  }}
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
                  onChange={isChecked => {
                    updateField({
                      field: "remove",
                      value: isChecked,
                    });
                  }}
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
                  type="number"
                  defaultValue={config["min-movie-size"] / mb}
                  onPressEnter={e =>
                    updateField({
                      field: "min-movie-size",
                      value: Number(e.target.value) * mb,
                    })}
                />
              </Col>
            </Row>
            <Row>
              <Col span={12}>
                <strong>Number subtitles</strong>
              </Col>
              <Col span={12}>
                <Input
                  type="number"
                  defaultValue={config["max-sub"]}
                  onPressEnter={e =>
                    updateField({
                      field: "max-sub",
                      value: Number(e.target.value),
                    })}
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
    updateListField: async ({ field, value, action }) => {
      await dispatch(updateConfigListField({ field, value, action }));
      message.info("Updated!");
    },
    updateField: async ({ field, value }) => {
      await dispatch(updateConfigField({ field, value }));

      message.info("Updated!");
    },
  };
};

const enhance = compose(
  Form.create(),
  connect(mapStateToProps, mapDispatchToProps)
);

export default enhance(SFConfigIndex);
