import { Button, Form, Input, Switch as UISwitch } from "antd";
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
          <div>
            <Form onSubmit={this.handleSubmit}>
              <FormItem {...formItemLayout} label="E-mail" hasFeedback>
                {getFieldDecorator("email", {
                  rules: [
                    {
                      type: "email",
                      message: "The input is not valid E-mail!",
                    },
                    {
                      required: true,
                      message: "Please input your E-mail!",
                    },
                  ],
                })(<Input />)}
              </FormItem>
            </Form>

            <FormRow>
              <strong>Movie Folders</strong>
              <div>
                {folders.map((folder, k) => {
                  return (
                    <MovieFolder src={folder} key={k}>
                      <RPCButton
                        name="Remove"
                        icon="trash"
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
              </div>
            </FormRow>
            <FormRow>
              <strong>Languages</strong>
              <div>
                {languages.map((lang, k) => {
                  return (
                    <MovieFolder src={lang} key={k}>
                      <RPCButton
                        name="Remove"
                        icon="trash"
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
              </div>
            </FormRow>
            <FormRow>
              <strong>Providers</strong>
              <div>
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
              </div>
            </FormRow>
            <FormRow>
              <strong>Force download subtitle</strong>
              <UISwitch
                checked={force}
                action={[configActions.updateField, "force"]}
              />
            </FormRow>
            <FormRow>
              <strong>Remove old subtitles if not found new subtitle</strong>
              <UISwitch
                checked={remove}
                action={[configActions.updateField, "remove"]}
              />
            </FormRow>
            <FormRow>
              <div>
                <strong>Min movie size (MB)</strong>
                <div>(to ignore sample videos)</div>
              </div>
              <div>
                <Input
                  value={config["min-movie-size"] / mb}
                  actionFunc={value => [
                    configActions.updateField,
                    "min-movie-size",
                    Number(value) * mb,
                  ]}
                />
              </div>
            </FormRow>
            <FormRow>
              <strong>Number subtitles</strong>
              <Input
                value={config["max-sub"]}
                action={[configActions.updateField, "max-sub"]}
              />
            </FormRow>
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
