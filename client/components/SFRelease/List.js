import React from 'react'
import { Link } from 'react-router'
import RestService from '../RestService'
import LanguageStats from './LanguageStats'
import RPCButton from '../RPCButton'
import SFConfigIndex from '../SFConfig/Index'
import _ from 'lodash'
import update from 'react-addons-update'
import Switch from '../Switch'
import SFReleaseFilter from './Filter'

export default class SFReleaseList extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      data: [],
      current: null,
      connectionError: false,
      loading: false,
      filter: {
        // empty: false
      }
    }
  }

  componentWillMount() {
    this.loadData()
  }

  async loadData() {
    try {
      this.setState({loading: true})

      let data = await RestService.load('release')
      // console.log(data)

      this.setState({data: data, connectionError: false, loading: false})
    } catch (promise) {
//      console.log('error', promise)
      this.setState({connectionError: true, loading: false})
    }
  }

  filter(item) {
    if (this.state.filter.empty) {
      return _.isEmpty(item.subtitles)
    }

    for (let lang of ["en", "vi"]) {
      let fieldName = `lang_${lang}`
      if (this.state.filter[fieldName]) {
        return !item.subtitles[lang] || item.subtitles[lang].length == 0
      }
    }

    return true
  }

  updateFilter(filter) {
    this.setState({filter: filter})
  }

  render() {

    return (
      <div className="box box-solid">
        <div className="box-header with-border">
          <h3 className="box-title">Movies</h3>

          <div className="box-tools">
            <button type="button" className="btn btn-box-tool" data-widget="collapse">
              <i className="fa fa-minus"></i>
            </button>

            <button type="button" className="btn btn-box-tool"
              onClick={this.loadData.bind(this)}>
              <i className="fa fa-refresh"></i>
            </button>

            <RPCButton query="release/scan-all" name="Scan All"
              onComplete={this.loadData.bind(this)}/>
          </div>
        </div>
        <div className="box-body">
          <SFReleaseFilter onChange={this.updateFilter.bind(this)}/>

          {this.state.data.filter(this.filter.bind(this)).map((item, k) => {
            let stateClass = ""
            if (_.isEmpty(item.subtitles)) {
              stateClass = " bg-warning"
            }
            return (
              <div key={k} className={"row row-hover row-list-item"+stateClass}>
                <div className="col-xs-12">
                    {item.name}
                </div>
                <div className="col-xs-6">
                  <LanguageStats data={item.subtitles} />
                </div>
                <div className="col-xs-6 pull-right">
                  <RPCButton query="release/download" params={{src: item.src, name: item.name}}
                    icon="download"
                    onComplete={this.loadData.bind(this)} name="Download" />
                  &nbsp;
                  <RPCButton query="release/remove-subtitle"
                    params={{src: item.src, name: item.name}}
                    icon="eraser"
                    onComplete={this.loadData.bind(this)} name="Remove Subtitles" />
                  &nbsp;
                  <a href={`https://subscene.com/subtitles/title?q=${item.title_query}&l=`}
                    target="subscence" className="btn btn-default">
                    <i className="fa fa-bug"></i> Subscene
                  </a>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    )
  }
}
