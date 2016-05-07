import React from 'react'
import { Link } from 'react-router'

export default class AdminLTE extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <div>
        {this.props.children}
      </div>
    )
  }
}
