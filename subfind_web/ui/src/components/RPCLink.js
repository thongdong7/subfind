import React from "react";
import { Icon, Spin } from "antd";
import RPC from "./RPC";

export default class RPCLink extends React.Component {
  render() {
    return (
      <RPC {...this.props}>
        {({ loading, icon, onClick, name }) =>
          <a onClick={onClick}>
            {loading ? <Spin /> : <Icon type={icon} />} {name}
          </a>}
      </RPC>
    );
  }
}
