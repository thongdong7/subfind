import React from 'react'
import { Link } from 'react-router'

export default class LanguageStats extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    let data = []
    for (let lang in this.props.data) {
      data.push({lang: lang, size: this.props.data[lang].length})
    }

    return (
      <div className="">
        {data.map((item, k) => {
          return (
            <div key={k}><strong>{item.lang}</strong> {item.size}</div>
          )
        })}
      </div>
    )
  }
}
