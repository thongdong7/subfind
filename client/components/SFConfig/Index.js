import React from 'react'
import Loading from '../Loading'
import RestService from '../RestService'
import update from 'react-addons-update'
import MovieFolder from './MovieFolder'

export default class SFConfigIndex extends React.Component {
  constructor(props) {
    super(props)

    this.state = {data: null, formData: {}, loading: false}
  }

  componentWillMount() {
    this.loadData()
  }

  async loadData() {
    this.setState({loading: true})

    let data = await RestService.load("config")

    this.setState({data: data, loading: false})
  }

  async addFolder(e) {
    e.preventDefault()

    this.updateConfig({
      'src-$push': this.state.formData.src
    })
  }

  async updateConfig(params) {
    this.setState({loading: true})
    let ret = await RestService.load("config/update", params)
    // console.log(ret);

    if (ret.ok === false) {
      console.warn(ret.message);
      this.setState({loading: false})
    } else {
      this.setState(update(this.state, {formData: {src: {$set: ''}}, data: {$set: ret}, loading: {$set: false} }))
    }
  }

  formChange(e) {
    // console.log(e.target);
    let field = e.target.name
    let value = e.target.value
    this.setState(update(this.state, {formData: {[field]: {$set: value}}}))
  }

  removeFolder(src) {
    // console.log('remove ', src);
    this.updateConfig({'src-$remove': src})
  }

  render() {
    // console.log('render', this.state.formData);
    let loading
    if (this.state.loading) {
      loading = (
        <Loading />
      )

    }
    let content
    if (this.state.data) {
      content = (
        <div>
          <div className="col-sm-2"><strong>Folders</strong></div>
          <div className="col-sm-10">
            {this.state.data.src.map((item, k) => {
              return (
                <MovieFolder src={item} key={k} onRemove={() => this.removeFolder(item)}/>
              )
            })}
            <form role="form" onSubmit={this.addFolder.bind(this)}
              onChange={this.formChange.bind(this)}>
              <div className="form-group">
                <input name="src" type="text" className="form-control"
                  value={this.state.formData.src || ''} />
              </div>
              <div className="form-group">
                <button type="submit" className="btn btn-default">Add</button>
              </div>
            </form>
          </div>
        </div>
      )
    }

    return (
      <div className="box box-solid">
        <div className="box-header with-border">
          <h3 className="box-title">SFConfig Title</h3>

          <div className="box-tools">
            <button type="button" className="btn btn-box-tool" data-widget="collapse"><i className="fa fa-minus"></i>
            </button>
          </div>
        </div>
        <div className="box-body">
          {loading}
          {content}

        </div>
      </div>
    )
  }
}
