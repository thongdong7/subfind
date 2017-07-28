import React from "react";
import { Button } from "antd";
import RPC from "./RPC";

export default class RPCButton extends React.Component {
  render() {
    return (
      <RPC {...this.props}>
        {({ loading, icon, onClick, name }) =>
          <Button onClick={onClick} loading={loading} icon={icon}>
            {name}
          </Button>}
      </RPC>
    );
  }
}
