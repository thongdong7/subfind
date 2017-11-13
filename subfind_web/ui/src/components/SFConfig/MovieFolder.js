import { Col, Row } from "antd";
import React from "react";

class MovieFolder extends React.Component {
  render() {
    return (
      <Row>
        <Col span={12}>{this.props.src}</Col>
        <Col span={12}>{this.props.children}</Col>
      </Row>
    );
  }
}

export default MovieFolder;
