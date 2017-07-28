import React from "react";
import { Icon, Spin } from "antd";

export default class RPCLink extends React.Component {
  constructor(props) {
    super(props);

    this.state = { loading: false };
  }

  onClick = async () => {
    this.setState({ loading: true });

    const { params } = this.props;
    var esc = encodeURIComponent;
    var query = Object.keys(params)
      .map(k => esc(k) + "=" + esc(params[k]))
      .join("&");
    const url = this.props.query + "?" + query;
    console.log("url", url);
    let res = await fetch(url);
    let data = await res.json();

    this.setState({ loading: false });

    if (this.props.onComplete) {
      this.props.onComplete(data);
    }
  };

  render() {
    const { name, icon } = this.props;
    let loading;
    if (this.state.loading) {
      loading = <Spin />;
    } else {
      loading = <Icon type={icon} />;
    }

    return (
      <a onClick={this.onClick}>
        {loading} {name}
      </a>
    );

    // return React.createElement(
    //   tag,
    //   props,
    //   loading,
    //   icon,
    //   " " + this.props.name
    // );
  }
}
