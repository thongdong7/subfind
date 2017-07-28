import React from "react";

export default class RPC extends React.Component {
  constructor(props) {
    super(props);

    this.state = { loading: false };
  }

  onClick = async () => {
    this.setState({ loading: true });

    const { params = {} } = this.props;
    var esc = encodeURIComponent;
    var query = Object.keys(params)
      .map(k => esc(k) + "=" + esc(params[k]))
      .join("&");
    const url = this.props.query + "?" + query;
    // console.log("url", url);
    let res = await fetch(url);
    let data = await res.json();

    this.setState({ loading: false });

    if (this.props.onComplete) {
      this.props.onComplete(data);
    }
  };

  render() {
    const { name, icon, children } = this.props;

    return children({
      loading: this.state.loading,
      icon,
      onClick: this.onClick,
      name,
    });
  }
}
