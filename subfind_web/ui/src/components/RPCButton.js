import { Button } from "antd";
import React from "react";
import RPC from "./RPC";

export default class RPCButton extends React.Component {
  render() {
    return (
      <RPC {...this.props}>
        {({ loading, icon, onClick, name }) => (
          <Button onClick={onClick} loading={loading} icon={icon}>
            {name}
          </Button>
        )}
      </RPC>
    );
  }
}
