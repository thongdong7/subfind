import React from 'react'
import Switch from '../Switch'
import update from 'react-addons-update'

export default class SFReleaseFilter extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      languages: ["en", "vi"],
      filter: {
        empty: false,
        lang_en: false,
        lang_vi: false,
      }
    }
  }

  async toggleFilter(fieldName) {
    await this.setState(update(this.state, {
      filter: {
        [fieldName]: {
          $set: !this.state.filter[fieldName]
        }
      }
    }))

    if (this.props.onChange) {
      this.props.onChange(this.state.filter)
    }
    console.log(this.state.filter);
  }

  render() {
    return (
      <div>
        <div className="row">
          <div className="col-md-6 col-xs-8">
            Only show missed subtitle release
          </div>
          <div className="col-md-6 col-xs-4">
            <Switch checked={this.state.filter.empty}
              onChange={() => this.toggleFilter('empty')} />
          </div>
        </div>
        {this.state.languages.map((lang, k) => {
          let filter_lang = `lang_${lang}`
          return (
            <div className="row" key={k}>
              <div className="col-md-6 col-xs-8">
                Only show missed lang {lang}
              </div>
              <div className="col-md-6 col-xs-4">
                <Switch checked={this.state.filter[filter_lang]}
                  onChange={() => this.toggleFilter(filter_lang)} />
              </div>
            </div>
          )
        })}
      </div>
    )
  }
}
