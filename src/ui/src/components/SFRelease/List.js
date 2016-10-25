import React from 'react'
import { Link } from 'react-router'
//import RestService from '../RestService'
import LanguageStats from './LanguageStats'
//import RemoteButton from '../RemoteButton'
//import SFConfigIndex from '../SFConfig/Index'
import _ from 'lodash'
import update from 'react-addons-update'
import Switch from '../Switch'
import SFReleaseFilter from './Filter'
import * as tb from 'tb-react'
import {releaseActions} from '../../actions/release'

let onBottom

window.onscroll = function(ev) {
  if ((window.innerHeight + window.scrollY + 100) >= document.body.offsetHeight) {
    if (onBottom) {
      onBottom()
    }
    // console.log('bottom');
  }
};

class SFReleaseList extends React.Component {
  constructor(props, context) {
    super(props, context)

    this.state = {
      data: [],
      filteredData: [],
      current: null,
      connectionError: false,
      loading: false,
      filter: {
        // empty: false
      },
      page: 1,
      maxPage: 1
    }

    this.limit = 20
  }

  componentWillMount() {
    onBottom = this.onBottom.bind(this)

    this.loadData()
  }

  onBottom() {
    if (this.state.page >= this.state.maxPage) {
      return
    }

    let nextPage = this.state.page + 1
    this.setState({
      page: nextPage,
      filteredData: this.filterData(this.state.data, this.state.filter, nextPage)
    })
    // console.log('b', nextPage);
  }

  async loadData() {
//    try {
//      this.setState({loading: true})
//
//      let data = await RestService.load('release')
//
//      let maxPage = data.length / this.limit
//
//      this.setState({
//        data: data,
//        filteredData: this.filterData(data, this.state.filter),
//        page: 1,
//        maxPage: maxPage,
//        connectionError: false,
//        loading: false
//      })
//    } catch (promise) {
//      if (promise.responseJSON && promise.responseJSON.code == 501) {
//        // Missed config file
//        this.context.router.push('/release/config')
//        return
//      }
//
//      this.setState({connectionError: true, loading: false})
//    }
  }

  filterData(data, filter, page) {
    if (page == undefined) {
      page = this.state.page
    }

    // console.log(page, this.limit);

    return data.filter((item) => this.doFilter(item, filter))      .slice(0, page * this.limit)
  }

  doFilter(item, filter1) {
    // console.log('a');
    if (filter1.empty) {
      return _.isEmpty(item.subtitles)
    }

    for (let lang of ["en", "vi"]) {
      let fieldName = `lang_${lang}`
      if (filter1[fieldName]) {
        return !item.subtitles[lang] || item.subtitles[lang].length == 0
      }
    }

    return true
  }

  updateFilter(filter) {
//    console.log('update filter', filter);
    let filteredData = this.filterData(this.state.data, filter)
    this.setState({filter: filter, filteredData: filteredData})
  }

  render() {
    // console.log('render', this.state.filteredData.length);
    // console.log('props', this.props);
    const {releases, reload, onScanComplete} = this.props
    return (
      <div className="box box-solid">
        <div className="box-header with-border">
          <h3 className="box-title">Movies</h3>

          <div className="box-tools">
            <tb.Button
              name="Reload"
              icon="refresh"
              type="info"
              onClick={reload}
            />

            <tb.RemoteButton
              url="Release/scan-all"
              name="Scan All"
              icon="tasks"
              onComplete={onScanComplete}
            />

            <tb.LinkButton
              to="/release/config"
              icon="cog"
              name="Setup"
            />
          </div>
        </div>
        <div className="box-body">
          <SFReleaseFilter onChange={this.updateFilter.bind(this)}/>

          {releases.map((item, k) => {
            let stateClass = ""
            if (_.isEmpty(item.subtitles)) {
              stateClass = " bg-warning"
            }
            return (
              <div key={k} className={"row row-hover row-list-item"+stateClass}>
                <div className="col-lg-10 col-xs-12">
                    {item.name}
                </div>
                <div className="col-lg-1 col-xs-10">
                  <LanguageStats data={item.subtitles} />
                </div>
                <div className="col-lg-1 col-xs-2">
                  <tb.RemoteButton
                    url="Release/download"
                    params={{src: item.src, name: item.name}}
                    icon="download"
                    onComplete={reload}
                    name="Download"
                    type="info"
                  />
                  <tb.RemoteButton
                    url="Release/remove-subtitle"
                    params={{src: item.src, name: item.name}}
                    icon="trash"
                    onComplete={reload}
                    name="Remove Subtitles"
                    type="danger"
                  />
                  <a href={`https://subscene.com/subtitles/title?q=${item.title_query}&l=`}
                    target="subscence">
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

SFReleaseList.contextTypes = {
    router: React.PropTypes.object
}


export default tb.connect2({
  start: (dispatch) => dispatch(releaseActions.load),
  props: ({releases}, ownProps, dispatch) => ({
    releases,
    reload: () => dispatch(releaseActions.load),
    onScanComplete: () => {
      dispatch(releaseActions.load)
      tb.success('Scan completed')
    }
  })
})(SFReleaseList)
